from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from models.user_model import db, User
from models.event_model import Event
from models.complaint_model import Complaint
from models.rating_model import Rating

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        return "Access Denied"

    total_users = User.query.filter_by(role="user").count()

    total_organizers = User.query.filter_by(
        role="organizer"
    ).count()

    pending_organizers = User.query.filter_by(
        role="organizer",
        is_approved=False
    ).count()

    total_events = Event.query.count()

    pending_events = Event.query.filter_by(
        status="pending"
    ).count()

    total_complaints = Complaint.query.count()

    total_ratings = Rating.query.count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_organizers=total_organizers,
        pending_organizers=pending_organizers,
        total_events=total_events,
        pending_events=pending_events,
        total_complaints=total_complaints,
        total_ratings=total_ratings
    )


# =========================
# ORGANIZER APPROVAL SYSTEM
# =========================

@admin.route("/pending-organizers")
@login_required
def pending_organizers():

    if current_user.role != "admin":
        return "Access Denied"

    organizers = User.query.filter_by(
        role="organizer",
        is_approved=False
    ).all()

    return render_template(
        "pending_organizers.html",
        organizers=organizers
    )


@admin.route("/approve-organizer/<int:user_id>")
@login_required
def approve_organizer(user_id):

    if current_user.role != "admin":
        return "Access Denied"

    organizer = User.query.filter_by(
        id=user_id,
        role="organizer"
    ).first_or_404()

    organizer.is_approved = True

    db.session.commit()

    flash(
        "Organizer approved successfully!",
        "success"
    )

    return redirect(
        url_for("admin.pending_organizers")
    )


@admin.route("/reject-organizer/<int:user_id>")
@login_required
def reject_organizer(user_id):

    if current_user.role != "admin":
        return "Access Denied"

    organizer = User.query.filter_by(
        id=user_id,
        role="organizer"
    ).first_or_404()

    db.session.delete(organizer)

    db.session.commit()

    flash(
        "Organizer rejected successfully!",
        "danger"
    )

    return redirect(
        url_for("admin.pending_organizers")
    )


# =========================
# EVENT APPROVAL SYSTEM
# =========================

@admin.route("/pending-events")
@login_required
def pending_events():

    if current_user.role != "admin":
        return "Access Denied"

    events = Event.query.filter_by(
        status="pending"
    ).all()

    return render_template(
        "pending_events.html",
        events=events
    )


@admin.route("/approve-event/<int:event_id>")
@login_required
def approve_event(event_id):

    if current_user.role != "admin":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    event.status = "approved"

    db.session.commit()

    flash(
        "Event approved successfully!",
        "success"
    )

    return redirect(
        url_for("admin.pending_events")
    )


@admin.route("/reject-event/<int:event_id>")
@login_required
def reject_event(event_id):

    if current_user.role != "admin":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    event.status = "rejected"

    db.session.commit()

    flash(
        "Event rejected successfully!",
        "danger"
    )

    return redirect(
        url_for("admin.pending_events")
    )


# =========================
# COMPLAINT MANAGEMENT
# =========================

@admin.route("/view-complaints")
@login_required
def view_complaints():

    if current_user.role != "admin":
        return "Access Denied"

    complaints = Complaint.query.order_by(
        Complaint.id.desc()
    ).all()

    return render_template(
        "view_complaints.html",
        complaints=complaints
    )


# =========================
# LOWER ORGANIZER RATING
# =========================

@admin.route("/lower-rating/<int:organizer_id>")
@login_required
def lower_rating(organizer_id):

    if current_user.role != "admin":
        return "Access Denied"

    ratings = Rating.query.filter_by(
        organizer_id=organizer_id
    ).all()

    for rating in ratings:
        rating.rating = 1

    complaints = Complaint.query.filter_by(
        organizer_id=organizer_id
    ).all()

    for complaint in complaints:
        complaint.status = "resolved"

    db.session.commit()

    flash(
        "Organizer rating reduced to 1 star!",
        "warning"
    )

    return redirect(
        url_for("admin.view_complaints")
    )


# =========================
# BAN ORGANIZER
# =========================

@admin.route("/ban-organizer/<int:organizer_id>")
@login_required
def ban_organizer(organizer_id):

    if current_user.role != "admin":
        return "Access Denied"

    organizer = User.query.filter_by(
        id=organizer_id,
        role="organizer"
    ).first_or_404()

    organizer.is_approved = False

    complaints = Complaint.query.filter_by(
        organizer_id=organizer_id
    ).all()

    for complaint in complaints:
        complaint.status = "resolved"

    db.session.commit()

    flash(
        "Organizer banned successfully!",
        "danger"
    )

    return redirect(
        url_for("admin.view_complaints")
    )