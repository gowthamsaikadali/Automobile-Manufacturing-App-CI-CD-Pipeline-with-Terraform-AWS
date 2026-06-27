from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Vehicle
from forms import VehicleForm

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory_bp.route("/")
@login_required
def index():
    search   = request.args.get("search", "")
    category = request.args.get("category", "")
    status   = request.args.get("status", "")

    query = Vehicle.query
    if search:
        query = query.filter(
            Vehicle.model_name.ilike(f"%{search}%") |
            Vehicle.model_code.ilike(f"%{search}%")
        )
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)

    vehicles = query.order_by(Vehicle.created_at.desc()).all()
    return render_template("inventory/index.html", vehicles=vehicles,
                           search=search, category=category, status=status)


@inventory_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if current_user.role not in ["admin", "manager"]:
        flash("Permission denied.", "danger")
        return redirect(url_for("inventory.index"))
    form = VehicleForm()
    if form.validate_on_submit():
        vehicle = Vehicle(
            model_name=form.model_name.data,
            model_code=form.model_code.data,
            category=form.category.data,
            year=form.year.data,
            color=form.color.data,
            price=form.price.data,
            stock=form.stock.data,
            status=form.status.data,
        )
        db.session.add(vehicle)
        db.session.commit()
        flash(f"Vehicle {vehicle.model_name} added.", "success")
        return redirect(url_for("inventory.index"))
    return render_template("inventory/form.html", form=form, title="Add Vehicle")


@inventory_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if current_user.role not in ["admin", "manager"]:
        flash("Permission denied.", "danger")
        return redirect(url_for("inventory.index"))
    vehicle = Vehicle.query.get_or_404(id)
    form = VehicleForm(obj=vehicle)
    if form.validate_on_submit():
        form.populate_obj(vehicle)
        db.session.commit()
        flash("Vehicle updated.", "success")
        return redirect(url_for("inventory.index"))
    return render_template("inventory/form.html", form=form, title="Edit Vehicle")


@inventory_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    if current_user.role != "admin":
        flash("Only admins can delete vehicles.", "danger")
        return redirect(url_for("inventory.index"))
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    flash("Vehicle deleted.", "success")
    return redirect(url_for("inventory.index"))
