const express = require("express");
const router = express.Router();

// Example: create ETH invoice
router.post("/create-eth-invoice", (req, res) => {
    const { amount, wallet } = req.body;
    // For testing, just return a dummy invoice
    res.json({ invoiceId: "ETH123", amount, wallet });
});

// Example: check payment
router.get("/check-eth-payment/:invoiceId", (req, res) => {
    const { invoiceId } = req.params;
    // Dummy response
    res.json({ invoiceId, paid: false });
});

module.exports = router;
