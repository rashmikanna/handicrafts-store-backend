#nosql models for notifications, admin log, error log

from mongoengine import Document, IntField, StringField, ListField, ReferenceField, BooleanField, DateTimeField
from datetime import datetime, timezone

class UserNotification(Document):
    user_id = StringField(required=True)
    title = StringField(required=True)
    message = StringField()
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    read = BooleanField(default=False)

    meta = {
        'collection': 'user_notifications',
        'ordering': ['-created_at']
    }

class AdminLog(Document):
    admin_id = StringField(required=True)
    action = StringField(required=True)  
    details = StringField()
    timestamp = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
    'collection': 'admin_logs',
    'ordering': ['-timestamp']
}

# Log backend errors, failures, etc.
class ErrorLog(Document):
    error_type = StringField(required=True)  
    message = StringField()
    occurred_at = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'error_logs',
        'ordering': ['-occurred_at']
    }