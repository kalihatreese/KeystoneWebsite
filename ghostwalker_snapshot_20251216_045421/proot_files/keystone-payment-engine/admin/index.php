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
