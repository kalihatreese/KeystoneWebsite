#!/bin/bash
# Ghostwalker Auto-Installer
# Path defaults
BASE_DIR="$HOME/KeystoneCreatorSuite/ghostwalker_snapshot_20251216_045421"
DIST_DIR="$HOME/KeystoneCreatorSuite/ghostwalker_dist"
PYTHON_BIN="$HOME/.termux-python/bin/python3"

echo "=== Ghostwalker Installer Starting ==="

# Ensure base directory exists
mkdir -p "$BASE_DIR" "$DIST_DIR"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found. Installing..."
    pkg install -y python
fi

# Check pip
if ! command -v pip &>/dev/null; then
    echo "pip not found. Installing..."
    python3 -m ensurepip
fi

# Install required Python packages
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy alembic pydantic redis rq stripe requests python-multipart python-jose email-validator jinja2

# Create virtual environment
VENV_DIR="$BASE_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Initialize directories
for DIR in apps infra ops sec payments auth data docs make tests deploy; do
    mkdir -p "$BASE_DIR/$DIR"
done

# Create environment file
ENV_FILE="$BASE_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
cat > "$ENV_FILE" <<EOL
# Ghostwalker environment defaults
BASE_DIR=$BASE_DIR
PYTHONPATH=$BASE_DIR
STRIPE_SECRET_KEY=dummy_key
DATABASE_URL=sqlite:///$BASE_DIR/ghostwalker.db
REDIS_URL=redis://localhost:6379/0
EOL
fi

# Python bootstrap script: run migrations, seed data, start API
BOOTSTRAP_PY="$BASE_DIR/bootstrap.py"
cat > "$BOOTSTRAP_PY" <<'PYTHONCODE'
import os
import sys
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

BASE_DIR = Path(os.getenv("BASE_DIR", Path.home() / "KeystoneCreatorSuite/ghostwalker_snapshot_20251216_045421"))

# Database setup
engine = create_engine(os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/ghostwalker.db"))
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(User).filter(User.email == "admin@ghostwalker.local").first():
        db.add(User(email="admin@ghostwalker.local", is_admin=True))
        db.commit()
    db.close()

# FastAPI app
app = FastAPI(title="Ghostwalker Core API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/admin")
def admin_info():
    return {"admin_email": "admin@ghostwalker.local"}

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8080)
PYTHONCODE

# Make executable
chmod +x "$BOOTSTRAP_PY"

echo "=== Ghostwalker Bootstrap Ready ==="
echo "Starting FastAPI service..."
"$PYTHON_BIN" "$BOOTSTRAP_PY" &
sleep 2
echo "Ghostwalker API running at http://127.0.0.1:8080"
echo "Admin user: admin@ghostwalker.local"
