import uuid
from flask import Flask, session

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mysecretkey"

    @app.before_request
    def ensure_guest_id():
        if "user_id" not in session:
            if "guest_id" not in session:
                session["guest_id"] = f"guest-{uuid.uuid4()}"

    from .routes import produk_bp, main_bp, auth_bp, cart_bp, checkout_bp, payment_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(produk_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(payment_bp)

    return app
