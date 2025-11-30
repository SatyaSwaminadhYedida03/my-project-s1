"""
Dead letter queue handler for failed tasks
"""

from backend.celery_config import celery_app
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DeadLetterQueue:
    """Handler for permanently failed tasks"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.dead_letter_queue
    
    def add(self, task_name, task_id, args, kwargs, exception, retries):
        """Add failed task to DLQ"""
        dlq_entry = {
            'task_name': task_name,
            'task_id': task_id,
            'args': args,
            'kwargs': kwargs,
            'exception': str(exception),
            'retries_attempted': retries,
            'failed_at': datetime.utcnow(),
            'status': 'pending_review',
            'reviewed': False
        }
        
        result = self.collection.insert_one(dlq_entry)
        logger.error(f"Task {task_name} ({task_id}) moved to DLQ after {retries} retries: {exception}")
        
        return result.inserted_id
    
    def get_pending(self, limit=100):
        """Get pending DLQ entries"""
        return list(self.collection.find({'status': 'pending_review'}).limit(limit))
    
    def mark_reviewed(self, dlq_id, action='discarded', notes=None):
        """Mark DLQ entry as reviewed"""
        update = {
            'reviewed': True,
            'reviewed_at': datetime.utcnow(),
            'action': action,
            'status': 'reviewed'
        }
        
        if notes:
            update['notes'] = notes
        
        self.collection.update_one({'_id': dlq_id}, {'$set': update})
    
    def retry_task(self, dlq_id):
        """Retry a failed task from DLQ"""
        entry = self.collection.find_one({'_id': dlq_id})
        
        if not entry:
            return {'status': 'error', 'message': 'DLQ entry not found'}
        
        # Get task from Celery
        task = celery_app.tasks.get(entry['task_name'])
        
        if not task:
            return {'status': 'error', 'message': 'Task not found in Celery'}
        
        # Retry task
        try:
            result = task.apply_async(args=entry['args'], kwargs=entry['kwargs'])
            
            # Update DLQ entry
            self.collection.update_one(
                {'_id': dlq_id},
                {
                    '$set': {
                        'retry_task_id': result.id,
                        'retried_at': datetime.utcnow(),
                        'status': 'retried'
                    }
                }
            )
            
            return {'status': 'success', 'task_id': result.id}
            
        except Exception as e:
            logger.error(f"Failed to retry task {entry['task_name']}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_stats(self):
        """Get DLQ statistics"""
        total = self.collection.count_documents({})
        pending = self.collection.count_documents({'status': 'pending_review'})
        reviewed = self.collection.count_documents({'status': 'reviewed'})
        retried = self.collection.count_documents({'status': 'retried'})
        
        # Top failing tasks
        pipeline = [
            {'$group': {'_id': '$task_name', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        top_failures = list(self.collection.aggregate(pipeline))
        
        return {
            'total': total,
            'pending': pending,
            'reviewed': reviewed,
            'retried': retried,
            'top_failures': top_failures
        }


@celery_app.task(name='process_dlq')
def process_dlq_task():
    """
    Periodic task to review and alert on DLQ entries
    (Can be scheduled in beat_schedule)
    """
    from backend.db import get_db
    
    db = get_db()
    dlq = DeadLetterQueue(db)
    
    stats = dlq.get_stats()
    
    if stats['pending'] > 0:
        logger.warning(f"DLQ has {stats['pending']} pending entries requiring review")
        
        # Could send alert email to admin
        # send_email_task.delay('admin@example.com', 'DLQ Alert', f"Pending entries: {stats['pending']}")
    
    return stats


# Export
__all__ = ['DeadLetterQueue', 'process_dlq_task']
