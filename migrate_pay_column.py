from app import create_app, db
from sqlalchemy import text
import logging

# Set up logging to see output clearly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

def migrate():
    with app.app_context():
        logger.info("Starting database migration: Adding 'accumulated_pay' column...")
        try:
            # PostgreSQL syntax: ALTER TABLE table_name ADD COLUMN IF NOT EXISTS column_name data_type
            # Since psycopg2/Postgres 9.6+ supports IF NOT EXISTS for columns
            db.session.execute(text("ALTER TABLE employees ADD COLUMN IF NOT EXISTS accumulated_pay FLOAT DEFAULT 0.0"))
            db.session.commit()
            logger.info("Successfully added 'accumulated_pay' column to 'employees' table.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Migration failed: {str(e)}")
            # Fallback for older Postgres versions if IF NOT EXISTS fails
            if "already exists" in str(e).lower():
                logger.info("Column already exists, skipping.")
            else:
                raise e

if __name__ == "__main__":
    migrate()
