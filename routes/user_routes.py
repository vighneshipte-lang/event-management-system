from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.event_model import Event
from models.user_model import db
from models.participation_model import Participation
from models.rating_model import Rating
from models.complaint_model import Complaint
from models.notification_model import Notification
from models.event_category_model import EventCategory
from models.team_model import Team
from models.schedule_model import Schedule
from datetime import datetime

user = Blueprint("user", __name__)


@user.route('/user-dashboard')
@login_required
def user_dashboard():

    if current_user.role != 'user':
        return "Access Denied"

    today = datetime.today().date()

    ongoing_events = Event.query.filter(
        Event.start_date <= today,
        Event.end_date >= today
    ).all()

    upcoming_events = Event.query.filter(
        Event.start_date > today
    ).all()

    notifications = Notification.query.all()

    participations = Participation.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        'user_dashboard.html',
        ongoing_events=ongoing_events,
        upcoming_events=upcoming_events,
        notifications=notifications,
        participations=participations
    )


@user.route('/view-events')
@login_required
def view_events():

    search = request.args.get('search')

    event_type = request.args.get('event_type')

    query = Event.query.filter_by(status='approved')

    # Search by title
    if search:

        query = query.filter(
            Event.title.ilike(f'%{search}%')
        )

    # Filter by event type
    if event_type and event_type != 'all':

        query = query.filter_by(
            event_type=event_type
        )

    events = query.all()

    return render_template(
        'view_events.html',
        events=events
    )


@user.route("/join-event/<int:event_id>")
@login_required
def join_event(event_id):

    if current_user.role != "user":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    # Only social events allowed
    if event.event_type != "social":

        flash("Only social events allow participation!", "danger")

        return redirect(url_for("user.view_events"))

    # Prevent duplicate joining
    existing = Participation.query.filter_by(
        user_id=current_user.id, event_id=event.id
    ).first()

    if existing:

        flash("Already joined this event!", "warning")

        return redirect(url_for("user.view_events"))

    # Save participation
    participation = Participation(user_id=current_user.id, event_id=event.id)

    db.session.add(participation)

    db.session.commit()

    flash("Joined event successfully!", "success")

    return redirect(url_for("user.view_events"))


@user.route("/my-participations")
@login_required
def my_participations():

    if current_user.role != "user":
        return "Access Denied"

    participations = Participation.query.filter_by(user_id=current_user.id).all()

    return render_template("my_participations.html", participations=participations)


@user.route("/rate-organizer/<int:event_id>", methods=["GET", "POST"])
@login_required
def rate_organizer(event_id):

    if current_user.role != "user":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    # Prevent duplicate rating
    existing_rating = Rating.query.filter_by(
        user_id=current_user.id, event_id=event.id
    ).first()

    if existing_rating:

        flash("You already rated this organizer!", "warning")

        return redirect(url_for("user.my_participations"))

    if request.method == "POST":

        rating_value = request.form["rating"]

        review = request.form["review"]

        new_rating = Rating(
            user_id=current_user.id,
            organizer_id=event.organizer_id,
            event_id=event.id,
            rating=rating_value,
            review=review,
        )

        db.session.add(new_rating)

        db.session.commit()

        flash("Rating submitted successfully!", "success")

        return redirect(url_for("user.my_participations"))

    return render_template("rate_organizer.html", event=event)


@user.route('/report-organizer/<int:event_id>', methods=['GET', 'POST'])
@login_required
def report_organizer(event_id):

    if current_user.role != 'user':
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':

        complaint_text = request.form['complaint_text']

        complaint = Complaint(
            user_id=current_user.id,
            organizer_id=event.organizer_id,
            event_id=event.id,
            complaint_text=complaint_text
        )

        db.session.add(complaint)

        db.session.commit()

        flash('Complaint submitted successfully!', 'success')

        return redirect(url_for('user.my_participations'))

    return render_template(
        'report_organizer.html',
        event=event
    )

@user.route('/notifications')
@login_required
def notifications():

    notifications = Notification.query.order_by(
        Notification.created_at.desc()
    ).all()

    return render_template(
        'notifications.html',
        notifications=notifications
    )

@user.route('/join-category/<int:category_id>')
@login_required
def join_category(category_id):

    if current_user.role != 'user':
        return "Access Denied"

    category = EventCategory.query.get_or_404(category_id)

    # Prevent duplicate registration
    existing_participation = Participation.query.filter_by(
        user_id=current_user.id,
        category_id=category.id
    ).first()

    if existing_participation:

        flash(
            'You already registered in this category!',
            'warning'
        )

        return redirect(
            url_for('user.view_events')
        )

    # Participant limit check
    total_participants = Participation.query.filter_by(
        category_id=category.id
    ).count()

    if total_participants >= category.max_participants:

        flash(
            'Participant limit reached!',
            'danger'
        )

        return redirect(
            url_for('user.view_events')
        )

    participation = Participation(
        user_id=current_user.id,
        event_id=category.event_id,
        category_id=category.id,
        status='pending'
    )

    db.session.add(participation)

    db.session.commit()

    flash(
        'Registered successfully!',
        'success'
    )

    return redirect(
        url_for('user.my_participations')
    )

@user.route('/create-team/<int:category_id>', methods=['GET', 'POST'])
@login_required
def create_team(category_id):

    if current_user.role != 'user':
        return "Access Denied"

    category = EventCategory.query.get_or_404(category_id)

    if category.registration_type != 'team':
        return "Invalid Category"

    if request.method == 'POST':

        team_name = request.form['team_name']

        # Create Team
        team = Team(
            team_name=team_name,
            leader_id=current_user.id,
            category_id=category.id
        )

        db.session.add(team)

        db.session.commit()

        # Register Team
        participation = Participation(
            user_id=current_user.id,
            event_id=category.event_id,
            category_id=category.id,
            team_id=team.id,
            status='pending'
        )

        db.session.add(participation)

        db.session.commit()

        flash(
            'Team registered successfully!',
            'success'
        )

        return redirect(
            url_for('user.my_participations')
        )

    return render_template(
        'create_team.html',
        category=category
    )

@user.route('/event-schedule/<int:event_id>')
@login_required
def event_schedule(event_id):

    event = Event.query.get_or_404(event_id)

    schedules = Schedule.query.filter_by(
        event_id=event.id
    ).order_by(
        Schedule.event_day,
        Schedule.start_time
    ).all()

    return render_template(
        'event_schedule.html',
        event=event,
        schedules=schedules
    )