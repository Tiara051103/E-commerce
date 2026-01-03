from flask import Blueprint, render_template

checkout_bp = Blueprint(
    "checkout",
    __name__,
    url_prefix="/checkout"
)

@checkout_bp.route("/")
def index():
    return render_template("pages/checkout/index.html")
