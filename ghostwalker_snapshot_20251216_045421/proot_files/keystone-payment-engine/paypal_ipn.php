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
