from app import create_app, db
import os

app = create_app()

def reset_database():
    with app.app_context():
        print("Cleaning up database...")
        # Drop all tables
        db.drop_all()
        # Create all tables fresh
        db.create_all()
        print("Database has been reset successfully.")

if __name__ == '__main__':
    # Double check confirmation if run from command line
    confirm = input("This will DELETE ALL DATA. Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        reset_database()
        print("Done. You can now re-run seed_data.py if needed.")
    else:
        print("Reset cancelled.")
