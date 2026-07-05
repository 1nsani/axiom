#!/bin/bash
set -e

AXIOM_PATH="/tmp/axiom"
AXIOM_KNOWLEDGE_PATH="/tmp/Axiom-knowledge"
REPO_AXIOM="https://github.com/1nsani/axiom.git"
REPO_KNOWLEDGE="https://github.com/1nsani/Axiom-knowledge.git"

echo "[BOOTSTRAP] Memulai setup lingkungan Axiom di Colab..."

# ========== 1. Clone atau pull repo ==========
if [ -d "$AXIOM_PATH/.git" ]; then
    echo "[BOOTSTRAP] Repo axiom ditemukan, git pull..."
    cd "$AXIOM_PATH" && git pull
else
    echo "[BOOTSTRAP] Cloning repo axiom..."
    git clone "$REPO_AXIOM" "$AXIOM_PATH"
fi

if [ -d "$AXIOM_KNOWLEDGE_PATH/.git" ]; then
    echo "[BOOTSTRAP] Repo Axiom-knowledge ditemukan, git pull..."
    cd "$AXIOM_KNOWLEDGE_PATH" && git pull
else
    echo "[BOOTSTRAP] Cloning repo Axiom-knowledge..."
    git clone "$REPO_KNOWLEDGE" "$AXIOM_KNOWLEDGE_PATH"
fi

# ========== 2. Instal dependensi SISTEM (untuk manimpango) ==========
echo "[BOOTSTRAP] Menginstal dependensi sistem (build tools, cairo, pango)..."
sudo apt-get update -qq
sudo apt-get install -y -qq build-essential python3-dev libcairo2-dev \
    libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev

# ========== 3. Instal dependensi Python ==========
echo "[BOOTSTRAP] Menginstal dependensi Python..."
cd "$AXIOM_PATH"
pip install -r requirements.txt -q
cd "$AXIOM_KNOWLEDGE_PATH"
pip install -r requirements.txt -q

# ========== 4. Cek dan instal texlive ==========
echo "[BOOTSTRAP] Memeriksa instalasi texlive..."
if ! dpkg -l | grep -q texlive-latex-extra; then
    echo "[BOOTSTRAP] texlive tidak terinstal. Menginstal..."
    sudo apt-get install -y -qq texlive texlive-latex-extra dvisvgm
else
    echo "[BOOTSTRAP] texlive sudah terinstal."
fi

# ========== 5. Verifikasi environment ==========
echo "[BOOTSTRAP] Memverifikasi environment..."
python3 "$AXIOM_PATH/src/verify_environment.py"
echo "[BOOTSTRAP] Setup selesai. Environment siap digunakan."
