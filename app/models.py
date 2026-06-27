from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80),  unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(20),  default="viewer")   # admin / manager / viewer
    created_at = db.Column(db.DateTime,    default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id            = db.Column(db.Integer, primary_key=True)
    model_name    = db.Column(db.String(100), nullable=False)
    model_code    = db.Column(db.String(50),  unique=True, nullable=False)
    category      = db.Column(db.String(50),  nullable=False)   # Sedan / SUV / Truck etc.
    year          = db.Column(db.Integer,     nullable=False)
    color         = db.Column(db.String(50))
    price         = db.Column(db.Float,       nullable=False)
    stock         = db.Column(db.Integer,     default=0)
    status        = db.Column(db.String(20),  default="available")  # available / sold / reserved
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime,    default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Vehicle {self.model_name} ({self.model_code})>"


class ProductionOrder(db.Model):
    __tablename__ = "production_orders"

    id             = db.Column(db.Integer, primary_key=True)
    order_number   = db.Column(db.String(50),  unique=True, nullable=False)
    vehicle_id     = db.Column(db.Integer,     db.ForeignKey("vehicles.id"), nullable=False)
    quantity       = db.Column(db.Integer,     nullable=False, default=1)
    status         = db.Column(db.String(30),  default="planned")
    # planned / in_progress / completed / cancelled
    priority       = db.Column(db.String(10),  default="normal")   # low / normal / high
    start_date     = db.Column(db.Date)
    end_date       = db.Column(db.Date)
    notes          = db.Column(db.Text)
    created_by     = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vehicle        = db.relationship("Vehicle", backref="production_orders")
    creator        = db.relationship("User",    backref="production_orders")

    def __repr__(self):
        return f"<ProductionOrder {self.order_number}>"
