from models import db, user_datastore
from app import create_app
from flask_security import Security  # Import Security to initialize extension

app, _ = create_app()

with app.app_context():
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='User')
    db.session.commit()

    if not user_datastore.find_user(email="admin@abc.com"):
        print("Creating admin user")
        user_datastore.create_user(email="admin@abc.com", username="admin", password="#Appa2025", address = "admin", phone_number = 65435265214, roles=['admin'])
        db.session.commit()