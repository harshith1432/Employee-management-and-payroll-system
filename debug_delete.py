from app import create_app, db
from app.models.user import User, Employee
import sys

app = create_app()

with app.app_context():
    emp = Employee.query.first()
    if not emp:
        print("No employees found to delete.")
        sys.exit(0)
    
    print(f"Attempting to delete Employee: {emp.first_name} {emp.last_name} (ID: {emp.id})")
    
    user = User.query.get(emp.user_id)
    try:
        # Delete dependencies first for extra safety if cascade is failing
        # (Though SQLAlchemy should handle it)
        db.session.delete(emp)
        if user:
            print(f"Deleting associated User: {user.email}")
            db.session.delete(user)
        db.session.commit()
        print("SUCCESS: Record purged.")
    except Exception as e:
        db.session.rollback()
        print(f"FAILURE: {e}")
