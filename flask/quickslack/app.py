from flask import Flask, jsonify, render_template
from celery import Celery
from decouple import config
from slack_user_client import SlackClient

from quickslack.extensions import (
	debug_toolbar,
	db
)
from quickslack.routes.tests.api import test_api

CELERY_TASK_LIST = [
    'quickslack.tasks.example',
]

def create_celery_app(app=None):
    app = app or create_app()

    celery = Celery(
		app.import_name,
		broker=app.config['CELERY_BROKER_URL'],
		include=CELERY_TASK_LIST
	)

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(settings_override=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object('config.settings')

	app.config['slack'] = SlackClient(
		config('SLACK_EMAIL'),
		config('SLACK_PASSWORD'),
		config('SLACK_WORKSPACE_URL')
	)

	app.config['slack'].login()

	extensions(app)
	app.register_blueprint(test_api)

	@app.route('/')
	def index():
		return render_template('base.html')

	return app

def extensions(app):
	debug_toolbar.init_app(app)
	db.init_app(app)
	return None