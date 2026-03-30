from app import create_app, db, bcrypt
from app.models.user import User

app = create_app()

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@hrms.ai').first()
        if admin:
            print("Admin account already exists.")
            return

        # Create Admin
        admin = User(
            email='admin@hrms.ai',
            role='admin'
        )
        admin.set_password('Admin@2026')
        
        db.session.add(admin)
        db.session.commit()
        print("Admin account created successfully!")
        print("Email: admin@hrms.ai")
        print("Password: Admin@2026")

if __name__ == '__main__':
    create_admin()
