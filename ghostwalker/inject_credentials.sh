#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"

echo "🔑 Injecting Master Admin Credentials..."
cat > "$GW_ROOT/admin_credentials.json" << 'INNER_EOF'
{
  "admin_id": "ReeseDroid_Admin",
  "deployment_key": "B01E6864816C6E41",
  "security_salt": "GHOST_WALKER_2025_SECRET",
  "access_level": "OVERLORD",
  "status": "VERIFIED"
}
INNER_EOF

echo "📜 Injecting Ghost Walker Manual..."
cat > "$GW_ROOT/README.txt" << 'INNER_EOF'
==================================================
        GHOST WALKER: AUTONOMOUS OPERATOR
==================================================
ADMIN: ReeseDroid_Admin
KEY: B01E6864816C6E41

[SYSTEM OVERVIEW]
Ghost Walker is a self-aware, self-healing automation 
and monetization suite. It is authorized to scan, 
repair, and deploy within KeystoneCreatorSuite.

[CORE COMMANDS]
1. Start Services: bash bootstrap/install.sh
2. Stop Services:  bash bootstrap/stop.sh
3. Scan System:    python3 apps/scanner.py
4. View Revenue:   python3 apps/dashboard.py
5. Build Payload:  python3 apps/packager.py

[SECURITY]
Do not modify 'operator.json' or 'admin_credentials.json' 
without Admin authorization.
==================================================
INNER_EOF

echo "✅ Credentials and Manual are now live in $GW_ROOT"
