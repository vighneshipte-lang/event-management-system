from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.user_model import db, User
import bcrypt
from flask_login import login_required, current_user

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        # Prevent admin registration
        if role not in ["user", "organizer"]:
            flash("Invalid role selected!", "danger")
            return redirect(url_for("auth.register"))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.register"))

        # Encrypt password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Organizer requires approval
        approved = False

        if role == "user":
            approved = True

        # Create user
        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password.decode("utf-8"),
            role=role,
            is_approved=approved,
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")

        return redirect(url_for("auth.register"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Find user
        user = User.query.filter_by(email=email).first()

        # Check user exists
        if not user:
            flash("Invalid email or password!", "danger")
            return redirect(url_for("auth.login"))

        # Check password
        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):

            flash("Invalid email or password!", "danger")
            return redirect(url_for("auth.login"))

        # Organizer approval check
        if user.role == "organizer" and not user.is_approved:

            flash("Organizer account pending admin approval!", "warning")

            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Login successful!", "success")

        if user.role == "admin":
            return redirect(url_for('admin.admin_dashboard'))
        elif user.role == "organizer":
            return redirect(url_for('organizer.organizer_dashboard'))
        else:
            return redirect(url_for('user.user_dashboard'))

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully!", "success")

    return redirect(url_for("auth.login"))


@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]
        new_password = request.form["new_password"]

        # Find user
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found!", "danger")
            return redirect(url_for("auth.forgot_password"))

        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

        # Update password
        user.password = hashed_password.decode("utf-8")

        db.session.commit()

        flash("Password updated successfully!", "success")

        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    if request.method == 'POST':

        current_user.full_name = request.form['full_name']

        current_user.email = request.form['email']

        new_password = request.form['password']

        # Change password only if entered
        if new_password:

            hashed_password = bcrypt.hashpw(
                new_password.encode('utf-8'),
                bcrypt.gensalt()
            )

            current_user.password = hashed_password.decode('utf-8')

        db.session.commit()

        flash('Profile updated successfully!', 'success')

        return redirect(url_for('auth.profile'))

    return render_template(
        'profile.html'
    )