import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes import api

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    else:
        app.config.update(test_config)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    app.register_blueprint(api, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
