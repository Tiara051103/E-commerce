from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from payment.application.use_cases import (
    BuatPembayaranUseCase,
    KonfirmasiPembayaranUseCase
)

from payment.infrastructure.sqlite_db.payment_repository_sqlite import PaymentRepositorySqlite
from checkout.infrastructure.sqlite_db.checkout_repository_sqlite import CheckoutRepositorySqlite
from katalog.infrastructure.uuid.id_services import UuidGeneratorService

payment_bp = Blueprint("payment", __name__, url_prefix="/payment")

@payment_bp.route("/buat/<checkout_id>", methods=["GET", "POST"])
def buat_pembayaran(checkout_id):
    id_user = session.get("user_id")
    if not id_user:
        flash("Silakan login terlebih dahulu", "error")
        return redirect(url_for("auth.login"))

    checkout_repo = CheckoutRepositorySqlite()
    checkout = checkout_repo.get_by_id(checkout_id)

    if not checkout:
        flash("Checkout tidak ditemukan", "error")
        return redirect(url_for("cart.lihat_cart"))

    if request.method == "POST":
        metode = request.form.get("metode")
        bank = request.form.get("bank")  # optional

        if not metode:
            flash("Pilih metode pembayaran", "error")
            return redirect(request.url)

        uc = BuatPembayaranUseCase(
            checkout_repo=checkout_repo,
            payment_repo=PaymentRepositorySqlite(),
            id_service=UuidGeneratorService()
        )

        result = uc.execute(
            id_checkout=checkout_id,
            id_user=id_user,
            metode=metode,
            bank=bank
        )

        if not result.is_success:
            flash(result.message, "error")
            return redirect(request.url)

        flash("Pembayaran berhasil dibuat", "success")
        return redirect(
            url_for("payment.detail_pembayaran", payment_id=result.data.id)
        )

    # ⬇️ GET REQUEST
    return render_template(
        "pages/payment/pilih_metode.html",
        checkout=checkout
    )

# =====================================
# DETAIL PEMBAYARAN
# =====================================
@payment_bp.route("/detail/<payment_id>")
def detail_pembayaran(payment_id):
    payment_repo = PaymentRepositorySqlite()
    payment = payment_repo.get_by_id(payment_id)

    if not payment:
        flash("Data pembayaran tidak ditemukan", "error")
        return redirect(url_for("cart.lihat_cart"))

    return render_template(
        "pages/payment/detail_pembayaran.html",
        payment=payment
    )


# =====================================
# KONFIRMASI PEMBAYARAN (SIMULASI)
# =====================================
@payment_bp.route("/konfirmasi/<payment_id>", methods=["POST"])
def konfirmasi_pembayaran(payment_id):
    status = request.form.get("status")  # PAID / FAILED

    uc = KonfirmasiPembayaranUseCase(
        payment_repo=PaymentRepositorySqlite(),
        checkout_repo=CheckoutRepositorySqlite()
    )

    result = uc.execute(payment_id=payment_id, status=status)

    flash(
        result.message,
        "success" if result.is_success else "error"
    )

    return redirect(
        url_for("payment.detail_pembayaran", payment_id=payment_id)
    )