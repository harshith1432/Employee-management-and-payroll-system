from app import create_app, db
import os

app = create_app()

def cleanup():
    with app.app_context():
        print("Cleaning up database...")
        db.drop_all()
        db.create_all()
        print("Database has been reset successfully.")

if __name__ == '__main__':
    cleanup()
