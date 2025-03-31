from asgiref.sync import async_to_sync
from celery import Celery
from celery.schedules import crontab

import database.queries as db
from database.session import create_sessionmaker_instance
from config.config import REDIS_URL

celery_app = Celery('tasks', broker=REDIS_URL)

celery_app.conf.timezone = 'UTC'
celery_app.conf.enable_utc = True

celery_app.conf.beat_schedule = {
    "delete-unpopular-links-every-day": {
        "task": "tasks.tasks.delete_unpopular_links",
        "schedule": crontab(hour=0, minute=0),
    },
}

@celery_app.task
def delete_unpopular_links():
    async_to_sync(delete_unpopular_links_async)()

async def delete_unpopular_links_async():
    _, celery_sessionmaker = create_sessionmaker_instance()
    print(f"Deleting unpopular links")
    await db.delete_unpopular_links(sessionmaker=celery_sessionmaker)

@celery_app.task
def delete_link_at_time(link_id: int):
    async_to_sync(delete_link_at_time_async)(link_id)

async def delete_link_at_time_async(link_id: int):
    print(f"Deleting link with id {link_id}")
    _, celery_sessionmaker = create_sessionmaker_instance()
    await db.delete_url(link_id, sessionmaker=celery_sessionmaker)
