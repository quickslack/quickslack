from flask import Flask, jsonify, render_template
from celery import Celery
from decouple import config

from slack_user_client import SlackClient

from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from quickslack.routes.dashboard.views import dashboard
from quickslack.sentry import integrate_sentry
from quickslack.extensions import (
	debug_toolbar,
	db
)

import logging, logging.config, yaml
# logging.config.dictConfig(yaml.load(open('config/logging.conf')))
logging.config.fileConfig('config/logging.conf')

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
	# import sentry_sdk
	# sentry_sdk.init(
	# 	dsn=config('SENTRY_DNS'),
	# 	integrations=[FlaskIntegration()]
	# )
	integrate_sentry(FlaskIntegration)
	# sentry()

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object('config.flask')

	extensions(app)
	app.register_blueprint(dashboard)

	app.logger.info('Initializing Slack Client...')
	app.config['slack'] = SlackClient(
		config('SLACK_EMAIL'),
		config('SLACK_PASSWORD'),
		config('SLACK_WORKSPACE_URL')
	)
	app.logger.info('Logging into Slack...')
	app.config['slack'].login()

	@app.route('/')
	def index():
		return render_template('layouts/dashboard.html')

	@app.route('/debug_sentry')
	def trigger_error():
		division_by_zero = 1 / 0

	return app

def sentry():
	integrate_sentry(CeleryIntegration)
	integrate_sentry(RedisIntegration)
	integrate_sentry(SqlalchemyIntegration)


def extensions(app):
	app.logger = logging.getLogger('root')

	debug_toolbar.init_app(app)
	db.init_app(app)

	app.logger.info('Extensions started...')
	return None
