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
