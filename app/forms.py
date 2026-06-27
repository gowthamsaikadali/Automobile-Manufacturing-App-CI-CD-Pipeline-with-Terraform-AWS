from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, IntegerField, FloatField,
    SelectField, TextAreaField, DateField, SubmitField
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit   = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 80)])
    email    = StringField("Email",    validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6)])
    confirm  = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match")
    ])
    role     = SelectField("Role", choices=[
        ("viewer", "Viewer"), ("manager", "Manager"), ("admin", "Admin")
    ])
    submit   = SubmitField("Register")


class VehicleForm(FlaskForm):
    model_name = StringField("Model Name", validators=[DataRequired(), Length(1, 100)])
    model_code = StringField("Model Code", validators=[DataRequired(), Length(1, 50)])
    category   = SelectField("Category", choices=[
        ("Sedan", "Sedan"), ("SUV", "SUV"), ("Truck", "Truck"),
        ("Hatchback", "Hatchback"), ("Coupe", "Coupe"), ("Van", "Van")
    ])
    year       = IntegerField("Year",  validators=[DataRequired(), NumberRange(2000, 2030)])
    color      = StringField("Color",  validators=[Optional(), Length(max=50)])
    price      = FloatField("Price",   validators=[DataRequired(), NumberRange(min=0)])
    stock      = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    status     = SelectField("Status", choices=[
        ("available", "Available"), ("sold", "Sold"), ("reserved", "Reserved")
    ])
    submit     = SubmitField("Save Vehicle")


class ProductionOrderForm(FlaskForm):
    order_number = StringField("Order Number", validators=[DataRequired(), Length(1, 50)])
    vehicle_id   = SelectField("Vehicle",  coerce=int, validators=[DataRequired()])
    quantity     = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    status       = SelectField("Status", choices=[
        ("planned", "Planned"), ("in_progress", "In Progress"),
        ("completed", "Completed"), ("cancelled", "Cancelled")
    ])
    priority     = SelectField("Priority", choices=[
        ("low", "Low"), ("normal", "Normal"), ("high", "High")
    ])
    start_date   = DateField("Start Date", validators=[Optional()])
    end_date     = DateField("End Date",   validators=[Optional()])
    notes        = TextAreaField("Notes",  validators=[Optional()])
    submit       = SubmitField("Save Order")
