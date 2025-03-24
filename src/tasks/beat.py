from celery.schedules import crontab
from tasks.tasks import celery_app

celery_app.conf.beat_schedule = {
    "delete-expired-links-every-day": {
        "task": "tasks.cleanup.delete_expired_links",
        "schedule": crontab(hour=0, minute=0),
    },
}