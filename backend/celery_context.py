from celery import Task
from app import celery_app, create_app

app, _ = create_app()

class ContextTask(Task):

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

