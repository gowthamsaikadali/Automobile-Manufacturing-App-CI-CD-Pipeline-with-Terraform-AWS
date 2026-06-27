#!/bin/bash
set -e
exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

echo "===================================================="
echo "Automobile Manufacturing Application Bootstrap"
echo "Started at: $(date)"
echo "===================================================="

# ----------------------------------------------------
# Update System
# ----------------------------------------------------
dnf update -y

# ----------------------------------------------------
# Install Packages
# ----------------------------------------------------
dnf install -y \
    python3 \
    python3-pip \
    python3-devel \
    gcc \
    gcc-c++ \
    make \
    unzip \
    git

python3 --version
pip3 --version

# ----------------------------------------------------
# Create Application Directories
# ----------------------------------------------------
mkdir -p /var/www/automobile-app
mkdir -p /var/log/automobile-app
mkdir -p /etc/automobile-app

chown -R ec2-user:ec2-user /var/www/automobile-app
chown -R ec2-user:ec2-user /var/log/automobile-app

# ----------------------------------------------------
# Environment File
# ----------------------------------------------------
cat > /etc/automobile-app/env <<EOF
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://${db_username}:${db_password}@${db_host}:3306/${db_name}
SECRET_KEY=${secret_key}
AWS_REGION=ap-south-1
EOF

chmod 600 /etc/automobile-app/env

# ----------------------------------------------------
# Create Python Virtual Environment
# ----------------------------------------------------
cd /var/www/automobile-app

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip setuptools wheel

# ----------------------------------------------------
# Install Python Dependencies
# ----------------------------------------------------
if [ -f requirements.txt ]; then
    echo "Installing Python packages..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping package installation."
fi

# ----------------------------------------------------
# Run Database Seed
# ----------------------------------------------------
if [ -f seed.py ]; then
    echo "Running database seed..."
    python seed.py || true
else
    echo "seed.py not found. Skipping database seed."
fi

# ----------------------------------------------------
# Create Systemd Service
# ----------------------------------------------------
cat > /etc/systemd/system/automobile-app.service <<EOF
[Unit]
Description=Automobile Manufacturing Flask Application
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
EOF

# ----------------------------------------------------
# Enable Service
# ----------------------------------------------------
systemctl daemon-reload
systemctl enable automobile-app

# ----------------------------------------------------
# Start Service (Only if app exists)
# ----------------------------------------------------
if [ -f app.py ] || [ -f app/__init__.py ]; then
    echo "Starting application..."
    systemctl restart automobile-app || systemctl start automobile-app
    systemctl status automobile-app --no-pager || true
else
    echo "Application files not found. Service will be started after deployment."
fi

echo "===================================================="
echo "Bootstrap Completed Successfully"
echo "Finished at: $(date)"
echo "===================================================="