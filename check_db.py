from app import create_app, db
from sqlalchemy import inspect
import sys

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    columns = [c['name'] for c in inspector.get_columns('employees')]
    print("--- SCHEMA CHECK ---")
    print(f"Columns: {', '.join(columns)}")
    
    if 'is_verified' in columns:
        print("OK: 'is_verified' column exists.")
    else:
        print("MISSING: 'is_verified' column NOT found!")
    
    try:
        from app.models.user import Employee
        count = Employee.query.count()
        print(f"Employee Count: {count}")
    except Exception as e:
        print(f"QUERY ERROR: {e}")
    print("--- END CHECK ---")
