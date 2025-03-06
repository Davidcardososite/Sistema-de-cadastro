# __init__.py
import logging
from flask import Flask
from .config import Config
from .extensions import db




def create_app():
    
    # Inicializar o aplicativo Flask
    app = Flask(__name__)
    
    # Carregar configurações
    app.config.from_object(Config)
    
    
    

    # Inicializar extensões
    db.init_app(app)
    
    
    

    # Importar e registrar blueprints
    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    # Inicializar banco de dados
    with app.app_context():
        db.create_all()
        logging.info("Tabelas de banco de dados criadas com sucesso!")

    return app