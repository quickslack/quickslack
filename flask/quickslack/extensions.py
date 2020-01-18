from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import sentry_sdk
from decouple import config

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()

def integrate_sentry(func):
	sentry_sdk.init(
		config('SENTRY_DNS'),
		integrations=[func()]
	)