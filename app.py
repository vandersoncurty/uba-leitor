from flask import Flask
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'miboutech'

app.config['SESSION_TYPE'] = 'filesystem'  # ou 'redis', 'memcached', etc.
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
