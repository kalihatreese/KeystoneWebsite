#!/usr/bin/env bash
set -e

ROOT="${HOME}/keystone-payment-engine"
mkdir -p "$ROOT"
cd "$ROOT"

echo "[*] Creating Keystone Payment Engine at $ROOT"

#####################################
#  config.php
#####################################
cat > config.php <<'PHP'
<?php
// ==============================
// Keystone Payment Engine v1
// ==============================

// ---- CORE SETTINGS ----
// Public URL to this folder on your domain, NO trailing slash.
define('BASE_URL', 'https://www.keystoneaiml.com/pay');

define('DB_FILE', __DIR__ . '/keystone_payments.sqlite');
date_default_timezone_set('America/New_York');

// ---- STRIPE CONFIG ----
// Replace with your real Stripe keys.
define('STRIPE_SECRET_KEY', 'sk_live_xxx_replace_me');
define('STRIPE_WEBHOOK_SECRET', 'whsec_xxx_replace_me');

// ---- PAYPAL CONFIG ----
// Set to true when going live.
define('PAYPAL_LIVE', false);

define('PAYPAL_IPN_VERIFY_URL', PAYPAL_LIVE
    ? 'https://ipnpb.paypal.com/cgi-bin/webscr'
    : 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr');

// Your PayPal business email
define('PAYPAL_BUSINESS_EMAIL', 'your-paypal-email@example.com');

// ---- MAIL / RECEIPTS CONFIG ----
// Uses PHP mail() on Namecheap; SMTP_* kept for future expansion.
define('SMTP_HOST', 'smtp.gmail.com');
define('SMTP_PORT', 587);
define('SMTP_USER', 'your_gmail_username@gmail.com');
define('SMTP_PASS', 'your_app_password');
define('SMTP_FROM', 'noreply@keystoneaiml.com');
define('STORE_NAME', 'Keystone AI & ML');

// ---- PRODUCT CATALOG ----
// Map product_code -> [name, price, currency, file_path]
$KEYSTONE_PRODUCTS = [
    'OVERLORD_SNIPER' => [
        'name' => 'Overlord Sniper Vault',
        'price' => 249.00,
        'currency' => 'USD',
        'file_path' => __DIR__ . '/downloads/overlord_sniper.zip',
    ],
    'FULL_BUNDLE' => [
        'name' => 'Keystone Full Bundle Vault',
        'price' => 499.00,
        'currency' => 'USD',
        'file_path' => __DIR__ . '/downloads/full_bundle.zip',
    ],
    // Add more products here.
];
PHP

#####################################
#  db_init.php
#####################################
cat > db_init.php <<'PHP'
<?php
require __DIR__ . '/config.php';

function keystone_db() {
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO('sqlite:' . DB_FILE);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    return $pdo;
}

$db = keystone_db();

$db->exec("
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gateway TEXT NOT NULL,
    txn_id TEXT NOT NULL,
    email TEXT,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    product_code TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    raw_payload TEXT
);
");

$db->exec("
CREATE TABLE IF NOT EXISTS licenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id INTEGER NOT NULL,
    license_key TEXT NOT NULL UNIQUE,
    product_code TEXT NOT NULL,
    expires_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(payment_id) REFERENCES payments(id)
);
");

$db->exec("
CREATE TABLE IF NOT EXISTS downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    license_key TEXT NOT NULL,
    product_code TEXT NOT NULL,
    download_token TEXT NOT NULL UNIQUE,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    used_at TEXT
);
");

echo "[OK] Database initialized at " . DB_FILE . PHP_EOL;
PHP

#####################################
#  functions.php
#####################################
cat > functions.php <<'PHP'
<?php
require __DIR__ . '/config.php';

function keystone_db() {
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO('sqlite:' . DB_FILE);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    return $pdo;
}

function keystone_now() {
    return date('c');
}

function keystone_json($data, $code = 200) {
    http_response_code($code);
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

function keystone_random_token($len = 40) {
    return bin2hex(random_bytes($len / 2));
}

function keystone_get_product($code) {
    global $KEYSTONE_PRODUCTS;
    return $KEYSTONE_PRODUCTS[$code] ?? null;
}

function keystone_log_payment($gateway, $txn_id, $email, $amount, $currency, $product_code, $status, $raw_payload) {
    $db = keystone_db();
    $stmt = $db->prepare("
        INSERT INTO payments (gateway, txn_id, email, amount, currency, product_code, status, created_at, raw_payload)
        VALUES (:g, :t, :e, :a, :c, :p, :s, :created, :raw)
    ");
    $stmt->execute([
        ':g' => $gateway,
        ':t' => $txn_id,
        ':e' => $email,
        ':a' => $amount,
        ':c' => $currency,
        ':p' => $product_code,
        ':s' => $status,
        ':created' => keystone_now(),
        ':raw' => $raw_payload,
    ]);
    return keystone_db()->lastInsertId();
}

function keystone_issue_license($payment_id, $product_code, $days_valid = 365) {
    $db = keystone_db();
    $license = strtoupper('KSL-' . substr(keystone_random_token(24), 0, 24));
    $expires = (new DateTime())->modify("+$days_valid days")->format('c');
    $stmt = $db->prepare("
        INSERT INTO licenses (payment_id, license_key, product_code, expires_at, created_at)
        VALUES (:pid, :lk, :pc, :exp, :created)
    ");
    $stmt->execute([
        ':pid' => $payment_id,
        ':lk' => $license,
        ':pc' => $product_code,
        ':exp' => $expires,
        ':created' => keystone_now(),
    ]);
    return $license;
}

function keystone_create_download_token($license_key, $product_code, $hours_valid = 24) {
    $db = keystone_db();
    $token = keystone_random_token(40);
    $expires = (new DateTime())->modify("+$hours_valid hours")->format('c');
    $stmt = $db->prepare("
        INSERT INTO downloads (license_key, product_code, download_token, expires_at, created_at)
        VALUES (:lk, :pc, :tok, :exp, :created)
    ");
    $stmt->execute([
        ':lk' => $license_key,
        ':pc' => $product_code,
        ':tok' => $token,
        ':exp' => $expires,
        ':created' => keystone_now(),
    ]);
    return $token;
}

function keystone_get_license($license_key) {
    $db = keystone_db();
    $stmt = $db->prepare("SELECT * FROM licenses WHERE license_key = :lk");
    $stmt->execute([':lk' => $license_key]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}

function keystone_mark_download_used($token) {
    $db = keystone_db();
    $stmt = $db->prepare("UPDATE downloads SET used_at = :now WHERE download_token = :tok");
    $stmt->execute([':now' => keystone_now(), ':tok' => $token]);
}

// Simple mail wrapper using PHP mail(); Namecheap usually supports this.
function keystone_send_email($to, $subject, $body) {
    $headers = "From: " . SMTP_FROM . "\r\n" .
               "Reply-To: " . SMTP_FROM . "\r\n" .
               "Content-Type: text/plain; charset=UTF-8\r\n";
    return mail($to, $subject, $body, $headers);
}

function keystone_send_license_email($email, $product_name, $license_key, $download_url) {
    $subject = "[" . STORE_NAME . "] Your License & Download";
    $body = "Thank you for your purchase from " . STORE_NAME . "!\n\n"
          . "Product: $product_name\n"
          . "License Key: $license_key\n\n"
          . "Download Link (expires in 24 hours):\n$download_url\n\n"
          . "Keep this email safe.\n\n"
          . "- " . STORE_NAME . "\n";
    keystone_send_email($email, $subject, $body);
}
PHP

#####################################
#  stripe_webhook.php
#####################################
cat > stripe_webhook.php <<'PHP'
<?php
require __DIR__ . '/functions.php';

$payload = @file_get_contents('php://input');
$sig_header = $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '';

if (!$payload || !$sig_header) {
    keystone_json(['error' => 'Missing payload or signature'], 400);
}

$timestamp = null;
$v1 = null;
foreach (explode(',', $sig_header) as $part) {
    [$k, $v] = array_map('trim', explode('=', $part, 2));
    if ($k === 't') $timestamp = $v;
    if ($k === 'v1') $v1 = $v;
}
if (!$timestamp || !$v1) {
    keystone_json(['error' => 'Invalid signature header'], 400);
}

$expected_sig = hash_hmac('sha256', $timestamp . '.' . $payload, STRIPE_WEBHOOK_SECRET);
if (!hash_equals($expected_sig, $v1)) {
    keystone_json(['error' => 'Signature verification failed'], 400);
}

$event = json_decode($payload, true);
if (!$event) {
    keystone_json(['error' => 'Invalid JSON'], 400);
}

$type = $event['type'] ?? '';
$data = $event['data']['object'] ?? [];

if ($type === 'checkout.session.completed') {
    $session = $data;
    $client_email = $session['customer_details']['email'] ?? null;
    $amount_total = ($session['amount_total'] ?? 0) / 100.0;
    $currency = strtoupper($session['currency'] ?? 'USD');
    $product_code = $session['metadata']['product_code'] ?? null;
    $txn_id = $session['payment_intent'] ?? $session['id'];
} elseif ($type === 'payment_intent.succeeded') {
    $pi = $data;
    $client_email = $pi['charges']['data'][0]['billing_details']['email'] ?? null;
    $amount_total = ($pi['amount_received'] ?? 0) / 100.0;
    $currency = strtoupper($pi['currency'] ?? 'USD');
    $product_code = $pi['metadata']['product_code'] ?? null;
    $txn_id = $pi['id'] ?? null;
} else {
    keystone_json(['status' => 'ignored', 'event_type' => $type]);
}

if (!$product_code) {
    keystone_json(['error' => 'Missing product_code in metadata'], 400);
}

$product = keystone_get_product($product_code);
if (!$product) {
    keystone_json(['error' => 'Unknown product'], 400);
}

$payment_id = keystone_log_payment(
    'stripe',
    $txn_id,
    $client_email,
    $amount_total,
    $currency,
    $product_code,
    'completed',
    $payload
);

$license_key = keystone_issue_license($payment_id, $product_code);
$download_token = keystone_create_download_token($license_key, $product_code, 24);
$download_url = BASE_URL . '/download.php?token=' . urlencode($download_token);

if ($client_email) {
    keystone_send_license_email($client_email, $product['name'], $license_key, $download_url);
}

keystone_json([
    'status' => 'ok',
    'payment_id' => $payment_id,
    'license_key' => $license_key,
    'download_url' => $download_url,
]);
PHP

#####################################
#  paypal_ipn.php
#####################################
cat > paypal_ipn.php <<'PHP'
<?php
require __DIR__ . '/functions.php';

$raw_post_data = file_get_contents('php://input');
if (!$raw_post_data && !$_POST) {
    keystone_json(['error' => 'No POST data'], 400);
}

$req = 'cmd=_notify-validate';
foreach ($_POST as $key => $value) {
    $value = urlencode(stripslashes($value));
    $req .= "&$key=$value";
}

$ch = curl_init(PAYPAL_IPN_VERIFY_URL);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HEADER, false);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $req);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
$res = curl_exec($ch);
$err = curl_error($ch);
curl_close($ch);

if ($res !== 'VERIFIED') {
    keystone_log_payment('paypal', 'unverified', null, 0, 'USD', 'UNKNOWN', 'pending', $raw_post_data);
    keystone_json(['error' => 'IPN not verified', 'paypal_response' => $res, 'curl_error' => $err], 400);
}

$payment_status = $_POST['payment_status'] ?? '';
$receiver_email = $_POST['receiver_email'] ?? '';
$payer_email = $_POST['payer_email'] ?? '';
$mc_gross = (float)($_POST['mc_gross'] ?? 0);
$mc_currency = $_POST['mc_currency'] ?? 'USD';
$txn_id = $_POST['txn_id'] ?? '';
$custom = $_POST['custom'] ?? '';

if (strtolower(trim($receiver_email)) !== strtolower(PAYPAL_BUSINESS_EMAIL)) {
    keystone_json(['error' => 'Receiver email mismatch'], 400);
}

if (strtolower($payment_status) !== 'completed') {
    keystone_json(['status' => 'ignored', 'reason' => 'payment_status != completed']);
}

$product_code = $custom;
if (!$product_code) {
    keystone_json(['error' => 'Missing product_code in custom'], 400);
}

$product = keystone_get_product($product_code);
if (!$product) {
    keystone_json(['error' => 'Unknown product'], 400);
}

if (abs($mc_gross - $product['price']) > 0.01 || strtoupper($mc_currency) !== $product['currency']) {
    keystone_json(['error' => 'Amount or currency mismatch'], 400);
}

$payment_id = keystone_log_payment(
    'paypal',
    $txn_id,
    $payer_email,
    $mc_gross,
    $mc_currency,
    $product_code,
    'completed',
    $raw_post_data
);

$license_key = keystone_issue_license($payment_id, $product_code);
$download_token = keystone_create_download_token($license_key, $product_code, 24);
$download_url = BASE_URL . '/download.php?token=' . urlencode($download_token);

if ($payer_email) {
    keystone_send_license_email($payer_email, $product['name'], $license_key, $download_url);
}

keystone_json([
    'status' => 'ok',
    'payment_id' => $payment_id,
    'license_key' => $license_key,
    'download_url' => $download_url,
]);
PHP

#####################################
#  download.php
#####################################
cat > download.php <<'PHP'
<?php
require __DIR__ . '/functions.php';

$token = $_GET['token'] ?? '';
if (!$token) {
    http_response_code(400);
    echo "Missing token";
    exit;
}

$db = keystone_db();
$stmt = $db->prepare("SELECT * FROM downloads WHERE download_token = :tok");
$stmt->execute([':tok' => $token]);
$dl = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$dl) {
    http_response_code(404);
    echo "Invalid download token";
    exit;
}

$expires_at = new DateTime($dl['expires_at']);
$now = new DateTime();
if ($now > $expires_at) {
    http_response_code(410);
    echo "Download link expired";
    exit;
}

$license = keystone_get_license($dl['license_key']);
if (!$license) {
    http_response_code(404);
    echo "License not found";
    exit;
}

$product = keystone_get_product($dl['product_code']);
if (!$product || empty($product['file_path']) || !is_file($product['file_path'])) {
    http_response_code(500);
    echo "Product file not found";
    exit;
}

$file = $product['file_path'];
$filename = basename($file);
$filesize = filesize($file);

keystone_mark_download_used($token);

header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="' . $filename . '"');
header('Expires: 0');
header('Cache-Control: must-revalidate');
header('Pragma: public');
header('Content-Length: ' . $filesize);
readfile($file);
exit;
PHP

#####################################
#  license_check.php
#####################################
cat > license_check.php <<'PHP'
<?php
require __DIR__ . '/functions.php';

$key = $_GET['key'] ?? '';
$product = $_GET['product'] ?? '';

if (!$key || !$product) {
    keystone_json(['valid' => false, 'error' => 'Missing key or product'], 400);
}

$license = keystone_get_license($key);
if (!$license || $license['product_code'] !== $product) {
    keystone_json(['valid' => false, 'error' => 'License not found'], 404);
}

$expires = new DateTime($license['expires_at']);
$now = new DateTime();
if ($now > $expires) {
    keystone_json(['valid' => false, 'error' => 'License expired'], 410);
}

keystone_json([
    'valid' => true,
    'product' => $product,
    'expires_at' => $license['expires_at'],
]);
PHP

#####################################
#  admin/index.php
#####################################
mkdir -p admin
cat > admin/index.php <<'PHP'
<?php
require __DIR__ . '/../functions.php';

$db = keystone_db();
$payments = $db->query("SELECT * FROM payments ORDER BY id DESC LIMIT 50")->fetchAll(PDO::FETCH_ASSOC);
$licenses = $db->query("SELECT * FROM licenses ORDER BY id DESC LIMIT 50")->fetchAll(PDO::FETCH_ASSOC);
?>
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Keystone Payments Admin</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #040712; color: #f0f0f0; padding: 20px; }
    h1, h2 { color: #00e0ff; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 30px; font-size: 13px; }
    th, td { border: 1px solid #333; padding: 6px 8px; text-align: left; }
    th { background: #111824; }
    tr:nth-child(even) { background: #0a0f1a; }
    code { background: #111; padding: 2px 4px; border-radius: 3px; }
  </style>
</head>
<body>
  <h1>Keystone Payment Engine – Admin</h1>
  <p>DB file: <code><?php echo htmlspecialchars(DB_FILE); ?></code></p>

  <h2>Recent Payments</h2>
  <table>
    <tr>
      <th>ID</th><th>Gateway</th><th>Txn</th><th>Email</th>
      <th>Product</th><th>Amount</th><th>Status</th><th>Created</th>
    </tr>
    <?php foreach ($payments as $p): ?>
      <tr>
        <td><?php echo (int)$p['id']; ?></td>
        <td><?php echo htmlspecialchars($p['gateway']); ?></td>
        <td><?php echo htmlspecialchars($p['txn_id']); ?></td>
        <td><?php echo htmlspecialchars($p['email']); ?></td>
        <td><?php echo htmlspecialchars($p['product_code']); ?></td>
        <td><?php echo htmlspecialchars($p['amount'] . ' ' . $p['currency']); ?></td>
        <td><?php echo htmlspecialchars($p['status']); ?></td>
        <td><?php echo htmlspecialchars($p['created_at']); ?></td>
      </tr>
    <?php endforeach; ?>
  </table>

  <h2>Recent Licenses</h2>
  <table>
    <tr>
      <th>ID</th><th>Payment ID</th><th>License</th><th>Product</th><th>Expires</th><th>Created</th>
    </tr>
    <?php foreach ($licenses as $l): ?>
      <tr>
        <td><?php echo (int)$l['id']; ?></td>
        <td><?php echo (int)$l['payment_id']; ?></td>
        <td><code><?php echo htmlspecialchars($l['license_key']); ?></code></td>
        <td><?php echo htmlspecialchars($l['product_code']); ?></td>
        <td><?php echo htmlspecialchars($l['expires_at']); ?></td>
        <td><?php echo htmlspecialchars($l['created_at']); ?></td>
      </tr>
    <?php endforeach; ?>
  </table>
</body>
</html>
PHP

#####################################
#  downloads placeholder
#####################################
mkdir -p downloads
echo "[*] Put your product zip files in: $ROOT/downloads" > downloads/README.txt

echo "[*] Running DB init..."
php db_init.php || echo "Run manually: php db_init.php"

echo
echo "[OK] Keystone Payment Engine v1 scaffolded at $ROOT"
echo "Upload contents of this folder to: public_html/pay on keystoneaiml.com"
