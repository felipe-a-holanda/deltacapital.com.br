from .web import SeleniumBrowsing
from config import celery_app


@celery_app.task
def run_simulation(pk):
    SeleniumBrowsing().run(pk)
