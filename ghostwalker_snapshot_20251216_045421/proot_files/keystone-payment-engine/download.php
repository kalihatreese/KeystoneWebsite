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
