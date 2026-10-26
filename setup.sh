#!/usr/bin/env bash
set -e

# 1. Determine destination directory (Termux vs standard Linux/macOS)
if [ -n "$PREFIX" ]; then
    INSTALL_DIR="$PREFIX/bin"
elif [ -d "$HOME/.local/bin" ]; then
    INSTALL_DIR="$HOME/.local/bin"
elif [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

echo -e "\033[1;34m[*] Installing tools to $INSTALL_DIR...\033[0m"

# 2. Verify source files exist
for script in rapidev.py portward.py; do
    if [ ! -f "$script" ]; then
        echo -e "\033[1;31m[!] Error: $script not found in current directory!\033[0m"
        exit 1
    fi
done

# 3. Copy scripts to target path
cp rapidev.py "$INSTALL_DIR/rapidev"
cp portward.py "$INSTALL_DIR/portward"

# 4. Make them executable
chmod +x "$INSTALL_DIR/rapidev"
chmod +x "$INSTALL_DIR/portward"

# 5. Success Output
echo -e "\n\033[1;32m[✓] Setup Complete!\033[0m"
echo -e "----------------------------------------"
echo -e " \033[1m[1]\033[0m \033[36mrapidev\033[0m                -> Run remote git pulling only"
echo -e " \033[1m[2]\033[0m \033[36mrapidev -d [port]\033[0m      -> Forward port (default 5173) & Start Server"
echo -e " \033[1m[3]\033[0m \033[36mportward {port}\033[0m        -> Forward port separately (e.g., portward 5174)"
echo -e "----------------------------------------"
