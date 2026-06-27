from flask import Blueprint, render_template
from flask_login import login_required
from models import Vehicle, ProductionOrder
from extensions import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    total_vehicles   = Vehicle.query.count()
    total_stock      = db.session.query(db.func.sum(Vehicle.stock)).scalar() or 0
    active_orders    = ProductionOrder.query.filter_by(status="in_progress").count()
    completed_orders = ProductionOrder.query.filter_by(status="completed").count()

    recent_orders = (
        ProductionOrder.query
        .order_by(ProductionOrder.created_at.desc())
        .limit(5)
        .all()
    )
    low_stock = Vehicle.query.filter(Vehicle.stock < 5).all()

    return render_template(
        "dashboard/index.html",
        total_vehicles=total_vehicles,
        total_stock=total_stock,
        active_orders=active_orders,
        completed_orders=completed_orders,
        recent_orders=recent_orders,
        low_stock=low_stock,
    )
