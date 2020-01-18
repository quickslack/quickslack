from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import sentry_sdk
from decouple import config

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()

def integrate_sentry(func):
	sentry_sdk.init(
		dsn="https://03ad353c3be7476da4127b4ca0c27c30@sentry.io/1886176", #config('SENTRY_DNS'),
		integrations=[func()]
	)