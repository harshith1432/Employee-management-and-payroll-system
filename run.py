from app import create_app, db
from app.models.user import User

app = create_app()

def init_on_start():
    with app.app_context():
        # This will create tables if they don't exist
        db.create_all()
        
        # Create default admin if system is empty
        if not User.query.filter_by(role='admin').first():
            admin = User(email='admin@hrms.com', role='admin')
            admin.set_password('Admin@123')
            db.session.add(admin)
            db.session.commit()
            print("Database initialized and default admin created.")

if __name__ == '__main__':
    init_on_start()
    app.run(debug=True)
