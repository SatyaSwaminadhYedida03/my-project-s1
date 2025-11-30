"""
Email sending tasks
"""

from backend.celery_config import celery_app, SafeTask
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


@celery_app.task(base=SafeTask, bind=True, name='send_email')
def send_email_task(self, to_email, subject, body, html_body=None):
    """
    Send email asynchronously
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text body
        html_body: Optional HTML body
    """
    try:
        # SMTP configuration
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        from_email = os.getenv('FROM_EMAIL', smtp_username)
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Add plain text part
        msg.attach(MIMEText(body, 'plain'))
        
        # Add HTML part if provided
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        return {'status': 'sent', 'to': to_email, 'timestamp': datetime.utcnow().isoformat()}
        
    except Exception as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)


@celery_app.task(base=SafeTask, name='send_welcome_email')
def send_welcome_email(user_email, user_name):
    """Send welcome email to new users"""
    subject = "Welcome to Smart Hiring System!"
    body = f"""
    Hi {user_name},
    
    Welcome to Smart Hiring System! Your account has been successfully created.
    
    You can now:
    - Browse job postings
    - Apply to positions
    - Take skill assessments
    - Track your applications
    
    Best regards,
    Smart Hiring Team
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Welcome to Smart Hiring System!</h2>
            <p>Hi {user_name},</p>
            <p>Welcome to Smart Hiring System! Your account has been successfully created.</p>
            <h3>You can now:</h3>
            <ul>
                <li>Browse job postings</li>
                <li>Apply to positions</li>
                <li>Take skill assessments</li>
                <li>Track your applications</li>
            </ul>
            <p>Best regards,<br>Smart Hiring Team</p>
        </body>
    </html>
    """
    
    return send_email_task.delay(user_email, subject, body, html_body)


@celery_app.task(base=SafeTask, name='send_application_status_email')
def send_application_status_email(user_email, job_title, new_status):
    """Send email when application status changes"""
    subject = f"Application Update: {job_title}"
    body = f"""
    Your application for {job_title} has been updated.
    
    New Status: {new_status}
    
    You can view more details in your dashboard.
    
    Best regards,
    Smart Hiring Team
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Application Update</h2>
            <p>Your application for <strong>{job_title}</strong> has been updated.</p>
            <p><strong>New Status:</strong> {new_status}</p>
            <p>You can view more details in your dashboard.</p>
            <p>Best regards,<br>Smart Hiring Team</p>
        </body>
    </html>
    """
    
    return send_email_task.delay(user_email, subject, body, html_body)


@celery_app.task(base=SafeTask, name='send_quiz_invitation')
def send_quiz_invitation(user_email, user_name, quiz_title, quiz_link):
    """Send quiz invitation email"""
    subject = f"Assessment Invitation: {quiz_title}"
    body = f"""
    Hi {user_name},
    
    You have been invited to take an assessment: {quiz_title}
    
    Please click the link below to begin:
    {quiz_link}
    
    Best regards,
    Smart Hiring Team
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Assessment Invitation</h2>
            <p>Hi {user_name},</p>
            <p>You have been invited to take an assessment: <strong>{quiz_title}</strong></p>
            <p><a href="{quiz_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Start Assessment</a></p>
            <p>Best regards,<br>Smart Hiring Team</p>
        </body>
    </html>
    """
    
    return send_email_task.delay(user_email, subject, body, html_body)


@celery_app.task(base=SafeTask, name='send_daily_digest')
def send_daily_digest(hour=9):
    """
    Send daily digest to users with new job matches
    (Scheduled task - runs daily)
    """
    from backend.db import get_db
    
    db = get_db()
    users = db.users.find({'email_preferences.new_job_alerts': True})
    
    for user in users:
        # Find matching jobs (simplified)
        matching_jobs = db.jobs.find({'status': 'open'}).limit(5)
        
        if matching_jobs:
            subject = "Your Daily Job Matches"
            body = f"Hi {user['name']},\n\nHere are today's job matches..."
            
            send_email_task.delay(user['email'], subject, body)
    
    return {'status': 'completed', 'users_notified': users.count()}


# Export
__all__ = [
    'send_email_task',
    'send_welcome_email',
    'send_application_status_email',
    'send_quiz_invitation',
    'send_daily_digest'
]
