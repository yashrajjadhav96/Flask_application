from flask import render_template, request, redirect, url_for, flash, session
from .. import db
from ..models.user_model import User
import re

# ---------------- Register User ----------------
def register_user():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        address = request.form.get("address")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        # --- Basic Validation ---
        if not name or not username or not mobile or not email or not address or not password or not repassword:
            flash("All fields are required.")
            return redirect(url_for("auth.register"))

        # Name validation
        if not re.match(r"^[A-Za-z ]+$", name):
            flash("Name must contain only alphabets.")
            return redirect(url_for("auth.register"))

        # Mobile validation
        if not re.match(r"^[0-9]{10}$", mobile):
            flash("Mobile number must be 10 digits.")
            return redirect(url_for("auth.register"))

        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.")
            return redirect(url_for("auth.register"))

        # Password validation
        if len(password) < 6 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[\W_]", password):
            flash("Password must have ≥6 chars, include uppercase, lowercase & special character.")
            return redirect(url_for("auth.register"))

        # Password match
        if password != repassword:
            flash("Passwords do not match.")
            return redirect(url_for("auth.register"))

        # Duplicate check
        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for("auth.register"))

        # Save user
        user = User(name=name, username=username, mobile=mobile, email=email, address=address)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------------- Login ----------------
def login_user():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email:
            flash("Username and Email are required.")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(username=username, email=email).first()
        if user and user.check_password(password):
            # ✅ Clearing stale sessions before login
            session.clear()

            session["user_id"] = user.id
            session["username"] = user.username
            session["email"] = user.email

            # Role-based redirect
            if "@admin" in email:
                return redirect(url_for("auth.admin_dashboard"))
            elif "@emp" in email:
                return redirect(url_for("auth.employee_home"))
            else:
                return redirect(url_for("auth.home"))
        else:
            flash("Invalid credentials.")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


# ---------------- Forgot Password ----------------
def forgot_password():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        if not username or not email:
            flash("Username and Email are required.")
            return redirect(url_for("auth.forgot"))

        user = User.query.filter_by(username=username, email=email).first()
        if user:
            flash("Password reset link sent to your email.")
        else:
            flash("No user found with that username and email.")
        return redirect(url_for("auth.forgot"))

    return render_template("forgot.html")


# ---------------- Logout ----------------
def logout_user():
    # ✅ Completely clear session
    session.clear()

    # ✅ Additional session cleanup for safety
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)

    flash("You have been logged out.")
    return redirect(url_for("auth.login"))


# ---------------- Home Pages ----------------
def home_page():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("home.html", username=session.get("username"))


def admin_dashboard():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html", username=session.get("username"))


def employee_home():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("employee_home.html", username=session.get("username"))
