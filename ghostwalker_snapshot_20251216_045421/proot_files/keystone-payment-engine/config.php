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
