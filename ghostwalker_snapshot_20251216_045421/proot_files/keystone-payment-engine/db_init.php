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
