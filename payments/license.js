const crypto = require('crypto');
const HMAC_KEY = process.env.LICENSE_HMAC || 'devkey';
function genLicense(productId){
  const payload = productId + '|' + Date.now() + '|' + Math.random().toString(36).slice(2,8);
  const sig = crypto.createHmac('sha256', HMAC_KEY).update(payload).digest('hex');
  return payload + '|' + sig;
}
module.exports = { genLicense };
