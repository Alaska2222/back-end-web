from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from routs import student, teacher
from waitress import serve
from flask_socketio import SocketIO, emit
import socketio

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'LPNU students'})
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)
app.register_blueprint(student)
app.register_blueprint(teacher)


@socketio.on('connect')
def handle_connect():
    print(f"User connected")
    socketio.emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"User disconnected")
    
@socketio.on('message')
def handle_message(message):
    print(f"Message: {message}")
    emit('chat', {'data': message}, brodcast=True)

    
if __name__ == "__main__":
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)
