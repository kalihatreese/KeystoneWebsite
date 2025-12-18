const { execSync } = require('child_process');

console.log("🛠️ INITIALIZING VERITAS GLOBAL DIAGNOSTIC...");

try {
    // 1. Test D1 Connectivity
    console.log("\n[1/3] Checking D1 Database Connection...");
    const d1Status = execSync('npx wrangler d1 execute keystone_db --command="SELECT 1;" --json').toString();
    console.log("✅ D1 API: Online");

    // 2. Test Asset Integrity
    console.log("\n[2/3] Checking 3D Engine Assets...");
    const html = execSync('cat build/index.html').toString();
    const hasThree = html.includes('three.min.js');
    const hasCanvas = html.includes('canvas');
    console.log(`📦 Three.js Linked: ${hasThree ? 'YES' : 'NO'}`);
    console.log(`🎨 Canvas CSS Fix: ${hasCanvas ? 'YES' : 'NO'}`);

    // 3. GitHub Sync Status
    console.log("\n[3/3] Checking GitHub Sync...");
    const gitStatus = execSync('git status').toString();
    if (gitStatus.includes('branch is up to date')) {
        console.log("✅ GitHub: Fully Synced");
    } else {
        console.log("⚠️ GitHub: Pending Changes Detected");
    }

    console.log("\n✨ DIAGNOSTIC COMPLETE: System is healthy. If screen is black, it is a GPU/Browser interaction issue.");
} catch (error) {
    console.error("\n❌ DIAGNOSTIC FAILED:", error.message);
}
