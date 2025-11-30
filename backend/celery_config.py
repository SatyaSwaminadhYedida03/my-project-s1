"""
Celery configuration for background task processing
"""

from celery import Celery
from datetime import timedelta
import os

# Redis connection
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Initialize Celery
celery_app = Celery(
    'smart_hiring',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        'backend.tasks.email_tasks',
        'backend.tasks.resume_tasks',
        'backend.tasks.notification_tasks'
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task routing
    task_routes={
        'backend.tasks.email_tasks.*': {'queue': 'email'},
        'backend.tasks.resume_tasks.*': {'queue': 'resume'},
        'backend.tasks.notification_tasks.*': {'queue': 'notifications'},
    },
    
    # Task serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Task execution
    task_acks_late=True,  # Tasks are acknowledged after completion
    task_reject_on_worker_lost=True,  # Reject tasks if worker dies
    worker_prefetch_multiplier=1,  # One task at a time per worker
    
    # Task time limits
    task_soft_time_limit=300,  # 5 minutes soft limit
    task_time_limit=600,  # 10 minutes hard limit
    
    # Task retries
    task_autoretry_for=(Exception,),
    task_retry_kwargs={'max_retries': 3},
    task_retry_backoff=True,
    task_retry_backoff_max=600,  # Max 10 minutes between retries
    task_retry_jitter=True,  # Add randomness to avoid thundering herd
    
    # Result backend
    result_expires=3600,  # Results expire after 1 hour
    result_backend_transport_options={
        'master_name': 'mymaster',
        'visibility_timeout': 3600,
    },
    
    # Dead letter queue
    task_default_max_retries=3,
    task_default_retry_delay=60,  # 1 minute default delay
    
    # Beat schedule for periodic tasks
    beat_schedule={
        'cleanup-expired-tokens': {
            'task': 'backend.tasks.maintenance_tasks.cleanup_expired_tokens',
            'schedule': timedelta(hours=1),
        },
        'send-daily-digest': {
            'task': 'backend.tasks.email_tasks.send_daily_digest',
            'schedule': timedelta(days=1),
            'kwargs': {'hour': 9}  # Send at 9 AM UTC
        },
        'analyze-quiz-performance': {
            'task': 'backend.tasks.analytics_tasks.analyze_quiz_performance',
            'schedule': timedelta(hours=6),
        },
    },
    
    # Worker monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Logging
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s',
)

# Task base class with error handling
class SafeTask(celery_app.Task):
    """Base task with automatic error logging"""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log task failures"""
        print(f'Task {self.name} failed: {exc}')
        # Could also send alert to monitoring service
        
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log task retries"""
        print(f'Task {self.name} retrying: {exc}')
        
    def on_success(self, retval, task_id, args, kwargs):
        """Log task success"""
        print(f'Task {self.name} succeeded')


# Export
__all__ = ['celery_app', 'SafeTask']
