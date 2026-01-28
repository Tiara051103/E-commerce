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

    cart_uc = AmbilCartUseCase(CartRepositorySqlite(DB_PATH))
    cart_result = cart_uc.execute(id_user=id_user, guest_id=guest_id)

    cart = cart_result.data
    produk_repo = ProdukRepositorySqlite()

    items = []
    ringkasan = {"total_item": 0, "total_harga": 0}

    if cart:
        for item in cart.items:
            produk = produk_repo.get_by_id(item.id_produk)

            items.append({
                "id": item.id,
                "id_produk": item.id_produk,
                "nama_produk": item.nama_produk,
                "harga_satuan": item.harga_satuan,
                "jumlah": item.jumlah,
                "gambar": produk.gambar if produk else None
            })

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

    flash("Produk ditambahkan ke keranjang", "success")
    return redirect(url_for("produk.daftar_produk"))


# ===============================
# UBAH JUMLAH
# ===============================
@cart_bp.route("/ubah-jumlah", methods=["POST"])
def ubah_jumlah_item():
    id_user = session.get("user_id")
    guest_id = request.cookies.get("guest_id")

    id_produk = request.form.get("id_produk")
    jumlah = max(1, int(request.form.get("jumlah", 1)))

    cart_uc = AmbilCartUseCase(CartRepositorySqlite(DB_PATH))
    cart = cart_uc.execute(id_user=id_user, guest_id=guest_id).data

    if not cart:
        return "", 204

    uc = UbahJumlahItemCartUseCase(CartItemRepositorySqlite(DB_PATH))
    uc.execute(id_cart=cart.id, id_produk=id_produk, jumlah=jumlah)

    return "", 204


# ===============================
# HAPUS ITEM
# ===============================
@cart_bp.route("/hapus-item", methods=["POST"])
def hapus_item():
    id_user = session.get("user_id")
    guest_id = request.cookies.get("guest_id")
    id_produk = request.form.get("id_produk")

    cart_uc = AmbilCartUseCase(CartRepositorySqlite(DB_PATH))
    cart = cart_uc.execute(id_user=id_user, guest_id=guest_id).data

    if not cart:
        flash("Cart tidak ditemukan", "error")
        return redirect(url_for("cart.lihat_cart"))

    uc = HapusItemCartUseCase(CartItemRepositorySqlite(DB_PATH))
    uc.execute(id_cart=cart.id, id_produk=id_produk)

    flash("Item dihapus dari keranjang", "success")
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
