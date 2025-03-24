from celery import Celery

import database.queries as db

celery_app = Celery('tasks', broker='redis://localhost:6379')

celery_app.conf.timezone = 'UTC'
celery_app.conf.enable_utc = True

@celery_app.task
async def delete_expired_links():
    await db.delete_expired_links()

@celery_app.task
async def delete_link_at_time(link_id: int):
    print(f"Deleting link with id {link_id}")
    await db.delete_url(link_id)
