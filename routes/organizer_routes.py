from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user_model import db, User
from models.event_model import Event
from models.participation_model import Participation
from datetime import datetime
from models.expense_model import Expense
from models.performer_model import Performer
from models.rating_model import Rating
from models.complaint_model import Complaint
from models.notification_model import Notification
from models.event_category_model import EventCategory
from models.schedule_model import Schedule
from models.event_category_model import EventCategory

organizer = Blueprint("organizer", __name__)


@organizer.route("/organizer/dashboard")
@login_required
def organizer_dashboard():

    if current_user.role != "organizer":
        return "Access Denied"


    events = Event.query.filter_by(organizer_id=current_user.id).all()

    total_events = len(events)

    total_participants = 0

    total_expenses = 0

    total_performers = 0

    for event in events:

        # Social event participants
        total_participants += Participation.query.filter_by(event_id=event.id).count()

        # Fixed event performers
        total_performers += Performer.query.filter_by(event_id=event.id).count()

        expenses = Expense.query.filter_by(event_id=event.id).all()

        total_expenses += sum(expense.amount for expense in expenses)

    return render_template(
        "organizer_dashboard.html",
        events=events,
        total_events=total_events,
        total_participants=total_participants,
        total_performers=total_performers,
        total_expenses=total_expenses,
    )


@organizer.route("/create-event", methods=["GET", "POST"])
@login_required
def create_event():

    # Only organizers allowed
    if current_user.role != "organizer":
        return "Access Denied"

    if request.method == "POST":

        title = request.form["title"]

        description = request.form["description"]

        event_type = request.form["event_type"]

        venue = request.form["venue"]

        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()

        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()

        start_time = datetime.strptime(request.form["start_time"], "%H:%M").time()

        end_time = datetime.strptime(request.form["end_time"], "%H:%M").time()

        max_participants = request.form["max_participants"]

        # Social event can allow unlimited participants
        if max_participants == "":
            max_participants = None

        new_event = Event(
            title=title,
            description=description,
            event_type=event_type,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            max_participants=max_participants,
            organizer_id=current_user.id,
        )

        db.session.add(new_event)

        db.session.commit()

        flash("Event created successfully!", "success")

        return redirect(url_for("organizer.organizer_dashboard"))

    return render_template("create_event.html")


@organizer.route("/event-participants/<int:event_id>")
@login_required
def event_participants(event_id):

    if current_user.role != "organizer":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    # Organizer can only access own events
    if event.organizer_id != current_user.id:
        return "Access Denied"

    participants = Participation.query.filter_by(event_id=event.id).all()

    return render_template(
        "event_participants.html", event=event, participants=participants
    )


@organizer.route("/assign-performance/<int:participation_id>", methods=["GET", "POST"])
@login_required
def assign_performance(participation_id):

    if current_user.role != "organizer":
        return "Access Denied"

    participation = Participation.query.get_or_404(participation_id)

    event = Event.query.get(participation.event_id)

    # Security check
    if event.organizer_id != current_user.id:
        return "Access Denied"

    if request.method == "POST":

        performance_time = request.form["performance_time"]

        participation.performance_time = performance_time

        participation.status = "approved"

        db.session.commit()

        flash("Performance time assigned!", "success")

        return redirect(url_for("organizer.event_participants", event_id=event.id))

    return render_template("assign_performance.html", participation=participation)


@organizer.route("/add-expense/<int:event_id>", methods=["GET", "POST"])
@login_required
def add_expense(event_id):

    if current_user.role != "organizer":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    # Security check
    if event.organizer_id != current_user.id:
        return "Access Denied"

    if request.method == "POST":

        title = request.form["title"]

        amount = request.form["amount"]

        category = request.form["category"]

        description = request.form["description"]

        spent_on = datetime.strptime(request.form["spent_on"], "%Y-%m-%d").date()

        expense = Expense(
            organizer_id=current_user.id,
            event_id=event.id,
            title=title,
            amount=amount,
            category=category,
            description=description,
            spent_on=spent_on,
        )

        db.session.add(expense)

        db.session.commit()

        flash("Expense added successfully!", "success")

        return redirect(url_for("organizer.view_expenses", event_id=event.id))

    return render_template("add_expense.html", event=event)


@organizer.route("/view-expenses/<int:event_id>")
@login_required
def view_expenses(event_id):

    if current_user.role != "organizer":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        return "Access Denied"

    expenses = Expense.query.filter_by(event_id=event.id).all()

    total_expense = sum(expense.amount for expense in expenses)

    return render_template(
        "view_expenses.html",
        event=event,
        expenses=expenses,
        total_expense=total_expense,
    )


@organizer.route("/add-performer/<int:event_id>", methods=["GET", "POST"])
@login_required
def add_performer(event_id):

    if current_user.role != "organizer":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    # Security check
    if event.organizer_id != current_user.id:
        return "Access Denied"

    # Only fixed events allowed
    if event.event_type != "fixed":

        flash("Performers can only be added to fixed events!", "danger")

        return redirect(url_for("organizer.organizer_dashboard"))

    if request.method == "POST":

        performer_name = request.form["performer_name"]

        performance_title = request.form["performance_title"]

        performance_time = request.form["performance_time"]

        description = request.form["description"]

        performer = Performer(
            event_id=event.id,
            performer_name=performer_name,
            performance_title=performance_title,
            performance_time=performance_time,
            description=description,
        )

        db.session.add(performer)

        db.session.commit()

        flash("Performer added successfully!", "success")

        return redirect(url_for("organizer.view_performers", event_id=event.id))

    return render_template("add_performer.html", event=event)


@organizer.route("/view-performers/<int:event_id>")
@login_required
def view_performers(event_id):

    if current_user.role != "organizer":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        return "Access Denied"

    performers = Performer.query.filter_by(event_id=event.id).all()

    return render_template("view_performers.html", event=event, performers=performers)


@organizer.route("/edit-event/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):

    if current_user.role != "organizer":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    # Security check
    if event.organizer_id != current_user.id:
        return "Access Denied"

    if request.method == "POST":

        event.title = request.form["title"]

        event.description = request.form["description"]

        event.venue = request.form["venue"]

        event.event_type = request.form["event_type"]

        event.start_date = datetime.strptime(
            request.form["start_date"], "%Y-%m-%d"
        ).date()

        event.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()

        db.session.commit()

        flash("Event updated successfully!", "success")

        return redirect(url_for("organizer.organizer_dashboard"))

    return render_template("edit_event.html", event=event)


@organizer.route("/delete-event/<int:event_id>")
@login_required
def delete_event(event_id):

    if current_user.role != "organizer":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    # Security check
    if event.organizer_id != current_user.id:
        return "Access Denied"

    # Delete participations
    Participation.query.filter_by(event_id=event.id).delete()

    # Delete performers
    Performer.query.filter_by(event_id=event.id).delete()

    # Delete expenses
    Expense.query.filter_by(event_id=event.id).delete()

    # Delete ratings
    Rating.query.filter_by(event_id=event.id).delete()

    # Delete complaints
    Complaint.query.filter_by(event_id=event.id).delete()

    # Finally delete event
    db.session.delete(event)

    db.session.commit()

    flash("Event and related data deleted successfully!", "success")

    return redirect(url_for("organizer.organizer_dashboard"))


@organizer.route("/add-notification/<int:event_id>", methods=["GET", "POST"])
@login_required
def add_notification(event_id):

    if current_user.role != "organizer":
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        return "Access Denied"

    if request.method == "POST":

        title = request.form["title"]

        message = request.form["message"]

        notification = Notification(event_id=event.id, title=title, message=message)

        db.session.add(notification)

        db.session.commit()

        flash("Notification created successfully!", "success")

        return redirect(url_for("organizer.organizer_dashboard"))

    return render_template("add_notification.html", event=event)

@organizer.route('/add-category/<int:event_id>', methods=['GET', 'POST'])
@login_required
def add_category(event_id):

    if current_user.role != 'organizer':
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        return "Access Denied"

    if request.method == 'POST':

        category_name = request.form['category_name']

        registration_type = request.form['registration_type']

        prize_amount = request.form['prize_amount']

        max_participants = request.form['max_participants']

        category = EventCategory(
            event_id=event.id,
            category_name=category_name,
            registration_type=registration_type,
            prize_amount=prize_amount,
            max_participants=max_participants
        )

        db.session.add(category)

        db.session.commit()

        flash('Category added successfully!', 'success')

        return redirect(
            url_for('organizer.organizer_dashboard')
        )

    return render_template(
        'add_category.html',
        event=event
    )

@organizer.route('/add-schedule/<int:event_id>', methods=['GET', 'POST'])
@login_required
def add_schedule(event_id):

    if current_user.role != 'organizer':
        return "Access Denied"

    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        return "Access Denied"

    categories = EventCategory.query.filter_by(
        event_id=event.id
    ).all()

    if request.method == 'POST':

        category_id = request.form.get('category_id')

        participant_name = request.form['participant_name']

        stage_name = request.form['stage_name']

        event_day = datetime.strptime(
            request.form['event_day'],
            '%Y-%m-%d'
        ).date()

        start_time = datetime.strptime(
            request.form['start_time'],
            '%H:%M'
        ).time()

        end_time = datetime.strptime(
            request.form['end_time'],
            '%H:%M'
        ).time()

        schedule = Schedule(
            event_id=event.id,
            category_id=category_id if category_id else None,
            participant_name=participant_name,
            stage_name=stage_name,
            event_day=event_day,
            start_time=start_time,
            end_time=end_time
        )

        db.session.add(schedule)

        db.session.commit()

        flash(
            'Schedule added successfully!',
            'success'
        )

        return redirect(
            url_for('organizer.organizer_dashboard')
        )

    return render_template(
        'add_schedule.html',
        event=event,
        categories=categories
    )