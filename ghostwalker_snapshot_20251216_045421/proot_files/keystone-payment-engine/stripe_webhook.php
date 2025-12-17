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
