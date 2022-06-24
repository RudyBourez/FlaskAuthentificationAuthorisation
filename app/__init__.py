from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace import config_integration
from opencensus.ext.azure import metrics_exporter
from dotenv import load_dotenv
import os
# init SQLAlchemy so we can use it later in our models
load_dotenv()
db = SQLAlchemy()    
app = Flask(__name__)
middleware = FlaskMiddleware(app)
logger = logging.getLogger(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db.init_app(app)
    
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

logger.addHandler(AzureLogHandler(
    connection_string = os.getenv("InstrumentationKey="+os.getenv('CONNEXION_STRING')))
)
logger.setLevel(logging.INFO)
config_integration.trace_integrations(['sqlalchemy'])

exporter = metrics_exporter.new_metrics_exporter(
    enable_standard_metrics=False,
    connection_string="InstrumentationKey="+os.getenv('CONNEXION_STRING'))

from .models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))
# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)