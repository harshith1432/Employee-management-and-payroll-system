from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    print("Initializing database...")
    db.create_all()
    
    # Create default admin if not exists
    if not User.query.filter_by(email='admin@hrms.com').first():
        admin = User(email='admin@hrms.com', role='admin')
        admin.set_password('Admin@123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin created: admin@hrms.com / Admin@123")
    else:
        print("Admin user already exists.")
    
    print("Database initialized successfully!")
