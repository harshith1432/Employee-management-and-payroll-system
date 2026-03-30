from app import create_app
from app.extensions import db
from app.models.core import DailyAgenda
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Check if table exists
        db.session.execute(text("SELECT 1 FROM daily_agendas LIMIT 1"))
        print("Table 'daily_agendas' already exists.")
    except Exception:
        print("Creating 'daily_agendas' table...")
        db.create_all()
        print("Table created successfully!")
