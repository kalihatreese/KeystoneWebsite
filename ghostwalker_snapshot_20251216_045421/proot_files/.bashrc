# ============================
#   ReeseDroid Terminal Theme
# ============================

# Prompt: ReeseDroid (capital D) in Money Green
PS1="\[\e[1;32m\]ReeseDroid💰 \w \$\[\e[0m\] "

# Global color settings: Kobalt Blue output
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

# Ensure LS uses color
alias ls='ls --color=auto'

# Grep highlight color in Kobalt Blue
export GREP_COLOR='38;5;21'

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
export KEYSTONE_REESE_EFFECT="$HOME/Keystone-Core/branding/reese_effect.txt"
export PATH=$HOME/bin:$PATH
export PATH=/data/data/com.termux/files/home/bin:/data/data/com.termux/files/home/bin:/data/data/com.termux/files/home/.cargo/bin:/data/data/com.termux/files/usr/bin
KEY_FOLDER="$HOME/keystonecreator-suite/keys"; [ -d "$KEY_FOLDER" ] && for f in "$KEY_FOLDER"/*.env*; do [ -f "$f" ] && export $(grep -v "^#" "$f" | xargs); done
