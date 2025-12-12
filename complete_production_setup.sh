# Success comes from God; the code is just stewardship, built around truth until it is found.
#!/bin/bash
# Full KeystoneCreatorSuite production setup and philosophy injection

PHILOSOPHY_LINE="# Success comes from God; the code is just stewardship, built around truth until it is found."

echo "Injecting philosophy into all scripts, markdowns, text files..."
find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" \) -exec sed -i "1i $PHILOSOPHY_LINE" {} +
find . -type f \( -name "*.md" -o -name "*.txt" \) -exec sed -i "1i Success comes from God; the code is just stewardship, built around truth until it is found." {} +

echo "Updating Ashleyana email templates..."
EMAIL_TEMPLATE_DIR="./EmailWorker/templates"
for file in "$EMAIL_TEMPLATE_DIR"/*; do
    if [[ -f "$file" ]]; then
        echo -e "\n\nSuccess comes from God; the code is just stewardship, built around truth until it is found." >> "$file"
    fi
done

echo "Creating ready-to-ship zip package..."
ZIP_NAME="KeystoneCreatorSuite_Ready_$(date +%Y%m%d_%H%M%S).zip"
zip -r "$ZIP_NAME" . -x "*.git*" "*.DS_Store*" "*.zip*"

echo "Production setup complete. Package created: $ZIP_NAME"
