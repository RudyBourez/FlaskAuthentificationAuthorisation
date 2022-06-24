from flask import Flask
from flask_principal import Principal, RoleNeed, Permission, UserNeed, identity_loaded
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
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
principals = Principal(app)

admin_permission = Permission(RoleNeed('Admin'))

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') 

db.init_app(app)
    
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string = "InstrumentationKey="+os.getenv('CONNEXION_STRING'))
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

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
            
# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)