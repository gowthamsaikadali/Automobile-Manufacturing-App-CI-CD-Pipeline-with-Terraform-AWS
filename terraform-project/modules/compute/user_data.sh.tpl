#!/bin/bash
# Amazon Linux 2023 — Python 3.11 built-in, uses dnf not yum
set -e
exec > /var/log/user-data.log 2>&1

echo "=== Automobile Manufacturing App Bootstrap ==="
echo "Started: $(date)"

# ── System packages ────────────────────────────────────────────────
dnf update -y
dnf install -y python3 python3-pip python3-devel gcc unzip

# ── Verify Python version ──────────────────────────────────────────
echo "Python version: $(python3 --version)"

# ── App directories ────────────────────────────────────────────────
mkdir -p /var/www/automobile-app
mkdir -p /var/log/automobile-app
mkdir -p /etc/automobile-app
chown ec2-user:ec2-user /var/www/automobile-app /var/log/automobile-app

# ── Environment variables file ─────────────────────────────────────
cat > /etc/automobile-app/env << 'ENVEOF'
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://${db_username}:${db_password}@${db_host}:3306/${db_name}
SECRET_KEY=${secret_key}
AWS_REGION=ap-south-1
ENVEOF
chmod 600 /etc/automobile-app/env

# ── Systemd service ────────────────────────────────────────────────
cat > /etc/systemd/system/automobile-app.service << 'SVCEOF'
[Unit]
Description=Automobile Manufacturing Flask App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/var/www/automobile-app
EnvironmentFile=/etc/automobile-app/env
ExecStart=/var/www/automobile-app/venv/bin/gunicorn \
    --workers 2 \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile /var/log/automobile-app/access.log \
    --error-logfile /var/log/automobile-app/error.log \
    app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable automobile-app

echo "Bootstrap complete: $(date)"
echo "Waiting for CI/CD pipeline to deploy the application..."
