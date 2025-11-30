"""
Notification tasks
"""

from backend.celery_config import celery_app, SafeTask
from datetime import datetime


@celery_app.task(base=SafeTask, name='send_notification')
def send_notification(user_id, notification_type, message, data=None):
    """
    Send in-app notification
    
    Args:
        user_id: User ID to notify
        notification_type: Type of notification
        message: Notification message
        data: Additional data
    """
    from backend.db import get_db
    
    db = get_db()
    notification = {
        'user_id': user_id,
        'type': notification_type,
        'message': message,
        'data': data or {},
        'read': False,
        'created_at': datetime.utcnow()
    }
    
    result = db.notifications.insert_one(notification)
    
    # TODO: Send real-time notification via WebSocket
    
    return {'status': 'sent', 'notification_id': str(result.inserted_id)}


@celery_app.task(base=SafeTask, name='notify_new_application')
def notify_new_application(recruiter_id, job_title, candidate_name):
    """Notify recruiter of new application"""
    message = f"New application received for {job_title} from {candidate_name}"
    return send_notification(recruiter_id, 'new_application', message)


@celery_app.task(base=SafeTask, name='notify_quiz_result')
def notify_quiz_result(candidate_id, quiz_title, passed):
    """Notify candidate of quiz result"""
    status = "passed" if passed else "did not pass"
    message = f"You {status} the assessment: {quiz_title}"
    return send_notification(candidate_id, 'quiz_result', message)


@celery_app.task(base=SafeTask, name='notify_job_match')
def notify_job_match(candidate_id, job_title, match_score):
    """Notify candidate of job match"""
    message = f"New job match: {job_title} ({match_score}% match)"
    return send_notification(candidate_id, 'job_match', message, {'match_score': match_score})


# Export
__all__ = [
    'send_notification',
    'notify_new_application',
    'notify_quiz_result',
    'notify_job_match'
]
