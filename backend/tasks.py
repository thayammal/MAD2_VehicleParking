from app import celery_app
from celery_context import ContextTask
from celery import shared_task
from flask_mail import Message



# @celery_app.task()
# def celery_print(base=ContextTask):
#     print('Hello from Celery Task')
#     return "Task completed Successfully"

# @celery_app.task(base=ContextTask)
# def add(x,y):
#     print('Adding {x} and {y} ')
#     return x+y


# @celery_app.task(base=ContextTask)
# def query_lotdb():
#     from models import ParkingLot
#     lot_list = ParkingLot.query.first()
#     print(f"Prime Location {lot_list.prime_location_name}")
#     return lot_list.prime_location_name


# @celery_app.task(base=ContextTask)
# def send_a_mail():
#     address = 'admin@abc.com'
#     from mailing import mail
#     from flask_mail import Message

#     msg = Message(subject = 'Hello from Celery')
#     msg.body = "This is test email sent from a Celery task"
#     msg.recipients = [address]
#     msg.html = f"""
#     <html>
#         <body>
#             <h1> Hello from Celery </h1>
#             <p> this is test email form celery task. <p>
#             <i> hi {address} </i>
#         </body>
#     <html>"""
#     mail.send(msg)
#     print(f'Email sent to {address}')
#     return f'Email sent to {address}'

from datetime import date, datetime
from models import User, Reservation, ParkingLot
from mailing import mail
from flask_mail import Message


@shared_task()
def send_daily_email_reminders_and_new_lots():
    today = date.today()
    current_hour = datetime.now().hour
    sender = 'donot_reply@abc.com'

    # Check if any lot was created today
    new_lots = ParkingLot.query.filter(
        ParkingLot.created_at >= datetime.combine(today, datetime.min.time())
    ).all()
    notify_all = bool(new_lots)

    reminders_sent = 0
    for user in User.query.all():
        # optional per-user timing
        if getattr(user, 'reminder_hour', None) is not None and user.reminder_hour != current_hour:
            continue

        # reservation check
        has_reserved = Reservation.query.filter(
            Reservation.user_id == user.id,
            Reservation.parking_timestamp >= datetime.combine(today, datetime.min.time())
        ).first()

        if not has_reserved or notify_all:
            body = f"Hi {user.username or user.email}, "
            if notify_all:
                body += f"{len(new_lots)} new parking lot(s) were added today.\n"
            if not has_reserved:
                body += "You haven't booked a parking spot today. Please do so if needed."

            msg = Message(
                subject="Daily Parking Reminder",
                recipients=[user.email],
                body=body,
                sender=sender
            )
            mail.send(msg)
            reminders_sent += 1
            print(f"Email sent to {user.email}")

    return f"Reminders sent to {reminders_sent} users. New lots: {len(new_lots)}"


from celery import shared_task
from flask_mail import Message
from flask import current_app
from sqlalchemy import func
from datetime import datetime, date, timedelta

from models import User, Reservation, ParkingLot
from mailing import mail

@shared_task()
def send_monthly_report():
    app = current_app._get_current_object()
    sender = app.config.get('MAIL_DEFAULT_SENDER')
    today = date.today()
    first_of_month = today.replace(day=1)
    last_month_end = first_of_month - timedelta(days=1)
    first_of_last_month = last_month_end.replace(day=1)

    users = User.query.all()
    for user in users:
        # Fetch reservations in last month
        res = (
            Reservation.query
            .filter(Reservation.user_id == user.id,
                    Reservation.parking_timestamp >= first_of_last_month,
                    Reservation.parking_timestamp <= last_month_end)
        )

        total_bookings = res.count()
        total_spent = res.with_entities(func.sum(Reservation.parking_cost)).scalar() or 0.0

        # Most used lot
        lot_counts = (
            res.join(ParkingLot, ParkingLot.id == Reservation.lot_id)
               .with_entities(ParkingLot.prime_location_name, func.count().label('cnt'))
               .group_by(ParkingLot.id)
               .order_by(func.count().desc())
        ).first()
        most_used = lot_counts.prime_location_name if lot_counts else 'N/A'

        # Build HTML report
        report_html = f"""
        <html><body>
          <p>Hi {user.username or user.email},</p>
          <h3>Parking Activity Report for {first_of_last_month.strftime('%B %Y')}</h3>
          <ul>
            <li>Total bookings: {total_bookings}</li>
            <li>Total amount spent: ₹{total_spent:.2f}</li>
            <li>Most used lot: {most_used}</li>
          </ul>
          <p>Thank you for using our service.</p>
        </body></html>
        """

        msg = Message(
            subject=f"Your Parking Report – {first_of_last_month.strftime('%B %Y')}",
            recipients=[user.email],
            html=report_html,
            sender=sender
        )
        mail.send(msg)
        app.logger.info(f"Monthly report sent to {user.email}")

    return f"Reports sent to {len(users)} users"
