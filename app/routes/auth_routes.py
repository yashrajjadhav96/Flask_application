from flask import Blueprint
from ..controllers import auth_controller

auth = Blueprint("auth", __name__)

# Login route
auth.add_url_rule("/", view_func=auth_controller.login_user, methods=["GET", "POST"], endpoint="login")
auth.add_url_rule("/login", view_func=auth_controller.login_user, methods=["GET", "POST"], endpoint="login")

# Register route
auth.add_url_rule("/register", view_func=auth_controller.register_user, methods=["GET", "POST"], endpoint="register")

# Forgot password route
auth.add_url_rule("/forgot", view_func=auth_controller.forgot_password, methods=["GET", "POST"], endpoint="forgot")

# Logout route
auth.add_url_rule("/logout", view_func=auth_controller.logout_user, endpoint="logout")

# Normal Home
auth.add_url_rule("/home", view_func=auth_controller.home_page, endpoint="home")

# Admin Dashboard
auth.add_url_rule("/admin_dashboard", view_func=auth_controller.admin_dashboard, endpoint="admin_dashboard")

# Employee Home
auth.add_url_rule("/employee_home", view_func=auth_controller.employee_home, endpoint="employee_home")
