#!/bin/bash
# 1. Initialize Capacitor React project for mobile dashboard
npx create-react-app trinity-dashboard-mobile
cd trinity-dashboard-mobile
npm install @capacitor/core @capacitor/cli @capacitor/android @capacitor-community/blessed

# 2. Copy Trinity dashboard + blockchain-monitor.js
mkdir -p src/trinity
cp ~/KeystoneCreatorSuite/trinity/{index.js,blockchain-monitor.js,paypal-checkout.js} src/trinity/

# 3. Setup .env inside mobile project
cp ~/KeystoneCreatorSuite/trinity/.env .env

# 4. Add simple dashboard page (React + Blessed for terminal-style widgets)
cat << 'REACT_DASH' > src/App.js
import React, { useEffect } from 'react';
import './App.css';
import { spawn } from 'child_process';

function App() {
  useEffect(() => {
    const node = spawn('node', ['src/trinity/index.js']);
    node.stdout.on('data', (data) => console.log(data.toString()));
    node.stderr.on('data', (data) => console.error(data.toString()));
  }, []);
  return (
    <div className="App">
      <h1>Keystone Trinity Dashboard</h1>
      <pre id="log"></pre>
    </div>
  );
}
export default App;
REACT_DASH

# 5. Initialize Capacitor Android platform
npx cap init "Keystone Trinity Mobile" "com.keystone.trinity"
npx cap add android
npx cap copy android

# 6. Build Android APK
npm run build
npx cap copy android
npx cap open android
echo "Open Android Studio -> Build APK -> Run on device/emulator"
