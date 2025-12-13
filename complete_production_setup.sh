#!/bin/bash
# Full KeystoneCreatorSuite production setup and philosophy injection


echo "Injecting philosophy into all scripts, markdowns, text files..."
find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" \) -exec sed -i "1i $PHILOSOPHY_LINE" {} +

echo "Updating Ashleyana email templates..."
EMAIL_TEMPLATE_DIR="./EmailWorker/templates"
for file in "$EMAIL_TEMPLATE_DIR"/*; do
    if [[ -f "$file" ]]; then
    fi
done

echo "Creating ready-to-ship zip package..."
ZIP_NAME="KeystoneCreatorSuite_Ready_$(date +%Y%m%d_%H%M%S).zip"
zip -r "$ZIP_NAME" . -x "*.git*" "*.DS_Store*" "*.zip*"

echo "Production setup complete. Package created: $ZIP_NAME"
