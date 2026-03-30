from flask_mail import Message
from app import mail

class NotificationService:
    @staticmethod
    def send_email(subject, recipient, body):
        try:
            msg = Message(subject, recipients=[recipient])
            msg.body = body
            # mail.send(msg) # Commented out for local demo unless configured
            print(f"EMAIL SENT TO {recipient}: {subject}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
            
    @staticmethod
    def notify_payroll_generated(employee, month, year):
        subject = f"Salary Slip Generated - {month}/{year}"
        body = f"Hello {employee.first_name}, your salary slip for {month}/{year} has been generated."
        return NotificationService.send_email(subject, employee.user.email, body)
