from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from cart.application.use_cases import (
    AmbilCartUseCase,
    TambahItemCartUseCase,
    UbahJumlahItemCartUseCase,
    HapusItemCartUseCase,
    KosongkanCartUseCase
)
from cart.infrastructure.sqlite_db.cart_repository_sqlite import (
    CartRepositorySqlite,
    CartItemRepositorySqlite
)
from katalog.infrastructure.sqlite_db.produk_repository_sqlite import (
    ProdukRepositorySqlite
)
from cart.infrastructure.sqlite_db.db_settings import DB_PATH
from cart.domain.services.services import UUIDGeneratorService

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


# ===============================
# LIHAT CART
# ===============================
@cart_bp.route("/lihat_cart")
def lihat_cart():
    id_user = session.get("user_id")
    guest_id = request.cookies.get("guest_id")

    uc = AmbilCartUseCase(
        CartRepositorySqlite(DB_PATH)
    )

    hasil = uc.execute(
        id_user=id_user,
        guest_id=guest_id
    )

    cart = hasil.data

    ringkasan = {"total_item": 0, "total_harga": 0}
    items = []

    if cart:
        for item in cart.items:
            items.append(item)
            ringkasan["total_item"] += item.jumlah
            ringkasan["total_harga"] += item.harga_satuan * item.jumlah

    session["cart_total_items"] = ringkasan["total_item"]

    return render_template(
        "pages/cart/index.html",
        cart=cart,
        items=items,
        ringkasan=ringkasan
    )

# ===============================
# TAMBAH ITEM
# ===============================
@cart_bp.route("/tambah-item", methods=["POST"])
def tambah_item_cart():
    id_user = session.get("user_id")
    guest_id = request.cookies.get("guest_id")


    id_produk = request.form.get("id_produk")
    jumlah = int(request.form.get("jumlah", 1))

    uc = TambahItemCartUseCase(
        CartRepositorySqlite(DB_PATH),
        CartItemRepositorySqlite(DB_PATH),
        ProdukRepositorySqlite(),
        UUIDGeneratorService()
    )

    hasil = uc.execute(
        id_user=id_user,
        guest_id=guest_id,
        id_produk=id_produk,
        jumlah=jumlah
    )

    flash(hasil.message if hasil.message else "Item berhasil ditambahkan", "success" if hasil.is_success else "error")
    return redirect(url_for("cart.lihat_cart"))

@cart_bp.route("/ubah-jumlah", methods=["POST"])
def ubah_jumlah_item():
    id_user = session.get("user_id")
    guest_id = request.cookies.get("guest_id")

    id_produk = request.form.get("id_produk")
    jumlah = max(1, int(request.form.get("jumlah", 1)))

    # Ambil cart dulu
    cart_uc = AmbilCartUseCase(CartRepositorySqlite(DB_PATH))
    cart_result = cart_uc.execute(id_user=id_user, guest_id=guest_id)

    if not cart_result.data:
        flash("Cart tidak ditemukan", "error")
        return redirect(url_for("cart.lihat_cart"))

    cart = cart_result.data

    # Update jumlah item di DB
    uc = UbahJumlahItemCartUseCase(CartItemRepositorySqlite(DB_PATH))
    hasil = uc.execute(id_cart=cart.id, id_produk=id_produk, jumlah=jumlah)

    flash(hasil.message if hasil.message else "Jumlah berhasil diubah",
          "success" if hasil.is_success else "error")

    return redirect(url_for("cart.lihat_cart"))

# ===============================
# HAPUS ITEM
# ===============================
@cart_bp.route("/hapus-item", methods=["POST"])
def hapus_item():
    id_user = session.get("user_id")
    guest_id = request.cookies.get("guest_id")
    id_produk = request.form.get("id_produk")

    cart_uc = AmbilCartUseCase(
        CartRepositorySqlite(DB_PATH),
    )
    cart_result = cart_uc.execute(
        id_user=id_user,
        guest_id=guest_id
    )

    if not cart_result.data:
        flash("Cart tidak ditemukan", "error")
        return redirect(url_for("cart.lihat_cart"))

    cart = cart_result.data

    uc = HapusItemCartUseCase(
        CartItemRepositorySqlite(DB_PATH)
    )

    uc.execute(
        id_cart=cart.id,
        id_produk=id_produk
    )

    flash("Item berhasil dihapus", "success")
    return redirect(url_for("cart.lihat_cart"))


# ===============================
# KOSONGKAN CART
# ===============================
@cart_bp.route("/kosongkan", methods=["POST"])
def kosongkan_cart():
    id_user = session.get("user_id")
    guest_id = request.cookies.get("guest_id")

    uc = KosongkanCartUseCase(
        CartRepositorySqlite(DB_PATH),
        CartItemRepositorySqlite(DB_PATH)
    )

    uc.execute(
        id_user=id_user,
        guest_id=guest_id
    )

    session["cart_total_items"] = 0
    session.modified = True

    flash("Keranjang berhasil dikosongkan", "success")
    return redirect(url_for("cart.lihat_cart"))
