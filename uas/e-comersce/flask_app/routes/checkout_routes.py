from flask import Blueprint, render_template, redirect, request, url_for, flash, session

from checkout.application.use_cases import BuatCheckoutUseCase
from checkout.infrastructure.sqlite_db.checkout_repository_sqlite import (
    CheckoutRepositorySqlite,
    CheckoutItemRepositorySqlite
)
from cart.infrastructure.sqlite_db.cart_repository_sqlite import (
    CartRepositorySqlite,
    CartItemRepositorySqlite
)
from cart.application.use_cases import AmbilCartUseCase
from checkout.infrastructure.uuid.id_services import UuidGeneratorService
from payment.application.use_cases import (BuatPembayaranUseCase,
    KonfirmasiPembayaranUseCase)
from payment.infrastructure.sqlite_db.payment_repository_sqlite import PaymentRepositorySqlite
from cart.infrastructure.sqlite_db.db_settings import DB_PATH

checkout_bp = Blueprint("checkout", __name__, url_prefix="/checkout")

# ======================================================
# STEP 1 — DARI CART → HALAMAN CHECKOUT
# ======================================================
@checkout_bp.route("/pilih", methods=["POST"])
def checkout():
    id_user = session.get("user_id")
    if not id_user:
        flash("Silakan login terlebih dahulu", "error")
        return redirect(url_for("auth.login"))

    selected_items_raw = request.form.get("selected_items", "")
    selected_item_ids = selected_items_raw.split(",")

    if not selected_item_ids or selected_item_ids == [""]:
        flash("Pilih minimal 1 item untuk checkout", "error")
        return redirect(url_for("cart.lihat_cart"))

    cart_uc = AmbilCartUseCase(CartRepositorySqlite())
    cart_result = cart_uc.execute(id_user=id_user)

    if not cart_result.is_success:
        flash("Cart tidak ditemukan", "error")
        return redirect(url_for("cart.lihat_cart"))

    cart = cart_result.data

    # ✅ FILTER PAKAI ID CART ITEM
    items_checkout = [
        item for item in cart.items
        if str(item.id) in selected_item_ids
    ]

    if not items_checkout:
        flash("Item checkout tidak valid", "error")
        return redirect(url_for("cart.lihat_cart"))

    total_harga = sum(item.harga_satuan * item.jumlah for item in items_checkout)

    return render_template(
        "pages/checkout/checkout.html",
        items=items_checkout,
        total_harga=total_harga
    )


@checkout_bp.route("/buat", methods=["POST"])
def buat_checkout():
    id_user = session.get("user_id")
    if not id_user:
        flash("Silakan login terlebih dahulu", "error")
        return redirect(url_for("auth.login"))

    # Ambil item
    item_ids = request.form.getlist("item_id")
    if not item_ids:
        flash("Item checkout tidak ditemukan", "error")
        return redirect(url_for("cart.lihat_cart"))

    # Metode pembayaran
    metode = request.form.get("metode")
    bank = request.form.get("bank")  # optional

    if not metode:
        flash("Pilih metode pembayaran terlebih dahulu", "error")
        return redirect(request.referrer or url_for("cart.lihat_cart"))

    if metode == "TRANSFER" and not bank:
        flash("Pilih bank tujuan transfer terlebih dahulu", "error")
        return redirect(request.referrer or url_for("cart.lihat_cart"))

    # Ambil cart
    cart_uc = AmbilCartUseCase(CartRepositorySqlite(DB_PATH))
    cart_result = cart_uc.execute(id_user=id_user)

    if not cart_result.is_success:
        flash(cart_result.message, "error")
        return redirect(url_for("cart.lihat_cart"))

    cart = cart_result.data

    # Filter item checkout
    items_checkout = [
        item for item in cart.items
        if str(item.id) in item_ids
    ]
    if not items_checkout:
        flash("Item checkout tidak valid", "error")
        return redirect(url_for("cart.lihat_cart"))

    # Buat checkout
    uc = BuatCheckoutUseCase(
        checkout_repo=CheckoutRepositorySqlite(),
        checkout_item_repo=CheckoutItemRepositorySqlite(),
        cart_repo=CartRepositorySqlite(),
        cart_item_repo=CartItemRepositorySqlite(),
        id_service=UuidGeneratorService()
    )

    checkout_result = uc.execute(
        id_user=id_user,
        items=items_checkout,
        metode_pembayaran=metode
    )
    
    if not checkout_result.is_success:
        flash(checkout_result.message, "error")
        return redirect(url_for("cart.lihat_cart"))

    checkout = checkout_result.data

    # Buat Payment
    payment_uc = BuatPembayaranUseCase(
        checkout_repo=CheckoutRepositorySqlite(),
        payment_repo=PaymentRepositorySqlite(),
        id_service=UuidGeneratorService()
    )

    payment_result = payment_uc.execute(
        id_checkout=checkout.id,
        id_user=id_user,
        metode=metode
    )

    if not payment_result.is_success:
        flash(payment_result.message, "error")
        return redirect(url_for("cart.lihat_cart"))

    # langsung ke detail pembayaran
    return redirect(
        url_for("payment.detail_pembayaran", payment_id=payment_result.data.id)
    )


# ======================================================
# STEP 1.5 — REVIEW CHECKOUT (KEMBALI DARI PAYMENT)
# ======================================================
@checkout_bp.route("/review/<checkout_id>")
def review_checkout(checkout_id):
    id_user = session.get("user_id")
    if not id_user:
        flash("Silakan login terlebih dahulu", "error")
        return redirect(url_for("auth.login"))

    # Ambil checkout yang sudah dibuat
    checkout_repo = CheckoutRepositorySqlite()
    checkout = checkout_repo.get_by_id(checkout_id)

    if not checkout:
        flash("Checkout tidak ditemukan", "error")
        return redirect(url_for("cart.lihat_cart"))

    # Ambil item checkout
    items = checkout.items
    total_harga = sum(item.harga_satuan * item.jumlah for item in items)

    return render_template(
        "pages/checkout/checkout.html",
        items=items,
        total_harga=total_harga
    )
