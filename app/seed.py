"""
seed.py — Run once to create the admin user.

Usage:
    cd app/
    python seed.py
"""
from app import create_app
from extensions import db
from models import User

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@automobile.local",
            role="admin"
        )
        admin.set_password("Admin@1234")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created — username: admin  password: Admin@1234")
    else:
        print("ℹ️  Admin user already exists.")
