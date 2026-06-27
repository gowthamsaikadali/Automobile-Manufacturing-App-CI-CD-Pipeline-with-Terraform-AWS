from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import ProductionOrder, Vehicle
from forms import ProductionOrderForm

production_bp = Blueprint("production", __name__, url_prefix="/production")


@production_bp.route("/")
@login_required
def index():
    status = request.args.get("status", "")
    query  = ProductionOrder.query
    if status:
        query = query.filter_by(status=status)
    orders = query.order_by(ProductionOrder.created_at.desc()).all()
    return render_template("production/index.html", orders=orders, status=status)


@production_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if current_user.role not in ["admin", "manager"]:
        flash("Permission denied.", "danger")
        return redirect(url_for("production.index"))
    form = ProductionOrderForm()
    form.vehicle_id.choices = [
        (v.id, f"{v.model_name} ({v.model_code})")
        for v in Vehicle.query.all()
    ]
    if form.validate_on_submit():
        order = ProductionOrder(
            order_number=form.order_number.data,
            vehicle_id=form.vehicle_id.data,
            quantity=form.quantity.data,
            status=form.status.data,
            priority=form.priority.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            notes=form.notes.data,
            created_by=current_user.id,
        )
        db.session.add(order)
        db.session.commit()
        flash(f"Order {order.order_number} created.", "success")
        return redirect(url_for("production.index"))
    return render_template("production/form.html", form=form, title="New Production Order")


@production_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if current_user.role not in ["admin", "manager"]:
        flash("Permission denied.", "danger")
        return redirect(url_for("production.index"))
    order = ProductionOrder.query.get_or_404(id)
    form  = ProductionOrderForm(obj=order)
    form.vehicle_id.choices = [
        (v.id, f"{v.model_name} ({v.model_code})")
        for v in Vehicle.query.all()
    ]
    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.commit()
        flash("Order updated.", "success")
        return redirect(url_for("production.index"))
    return render_template("production/form.html", form=form, title="Edit Order")


@production_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    if current_user.role != "admin":
        flash("Only admins can delete orders.", "danger")
        return redirect(url_for("production.index"))
    order = ProductionOrder.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash("Order deleted.", "success")
    return redirect(url_for("production.index"))
