from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.event_model import Event
from models.user_model import db, User
from models.complaint_model import Complaint
from models.rating_model import Rating

admin = Blueprint("admin", __name__)


@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():

    if current_user.role != 'admin':
        return "Access Denied"

    total_users = User.query.filter_by(
        role='user'
    ).count()

    total_organizers = User.query.filter_by(
        role='organizer'
    ).count()

    total_events = Event.query.count()

    pending_events = Event.query.filter_by(
        status='pending'
    ).count()

    total_complaints = Complaint.query.count()

    total_ratings = Rating.query.count()

    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_organizers=total_organizers,
        total_events=total_events,
        pending_events=pending_events,
        total_complaints=total_complaints,
        total_ratings=total_ratings
    )

@admin.route("/pending-events")
@login_required
def pending_events():

    if current_user.role != "admin":
        return "Access Denied"

    events = Event.query.filter_by(status="pending").all()

    return render_template("pending_events.html", events=events)

@admin.route('/approve-event/<int:event_id>')
@login_required
def approve_event(event_id):

    if current_user.role != 'admin':
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    event.status = 'approved'

    db.session.commit()

    flash('Event approved successfully!', 'success')

    return redirect(url_for('admin.pending_events'))

@admin.route('/reject-event/<int:event_id>')
@login_required
def reject_event(event_id):

    if current_user.role != 'admin':
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    event.status = 'rejected'

    db.session.commit()

    flash('Event rejected!', 'danger')

    return redirect(url_for('admin.pending_events'))

@admin.route('/view-complaints')
@login_required
def view_complaints():

    if current_user.role != 'admin':
        return "Access Denied"

    complaints = Complaint.query.all()

    return render_template(
        'view_complaints.html',
        complaints=complaints
    )