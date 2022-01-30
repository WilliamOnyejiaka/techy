from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask,jsonify
from src.api.v1.models import db,serializer,search
from src.api.v1.routes.auth import auth
from src.api.v1.routes.videos import videos
from src.api.v1.routes.bookmarks import bookmarks
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger,swag_from
from src.config.swagger import swagger_config, template

def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config\\config.py')
	CORS(app, supports_credentials=True, resources={
		r"/*": {
			"origins": {
				"*",
			}
		}
	})

	db.app = app
	db.init_app(app)
	serializer.init_app(app)
	search.init_app(app)
	JWTManager(app)

	app.register_blueprint(auth)
	app.register_blueprint(videos)
	app.register_blueprint(bookmarks)

	Swagger(app, config=swagger_config, template=template)

	@app.get("/")
	@swag_from("./docs/short_url.yaml")
	def hello_world():
		return "hello world"

	@app.errorhandler(HTTP_404_NOT_FOUND)
	def handle_404(e):
		return jsonify({'error': 'not found'})

	@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
	def handle_404(e):
		return jsonify({'error': 'something went wrong, we are working on it'})
	
	return app
