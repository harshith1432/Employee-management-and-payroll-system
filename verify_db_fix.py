from app import create_app, db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

def verify():
    with app.app_context():
        logger.info("Verifying 'accumulated_pay' column presence...")
        try:
            # Simple check by selecting the column
            db.session.execute(text("SELECT accumulated_pay FROM employees LIMIT 1"))
            logger.info("VERIFICATION SUCCESS: 'accumulated_pay' column exists.")
        except Exception as e:
            logger.error(f"VERIFICATION FAILED: {str(e)}")
            exit(1)

if __name__ == "__main__":
    verify()
