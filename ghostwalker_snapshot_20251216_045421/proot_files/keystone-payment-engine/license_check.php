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
