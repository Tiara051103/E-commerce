from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mysecretkey"
    
    
    from .routes import produk_bp, main_bp, auth_bp, cart_bp, checkout_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(produk_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    return app

