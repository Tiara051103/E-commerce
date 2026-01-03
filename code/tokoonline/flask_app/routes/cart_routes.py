from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from cart.domain.entities import Cart, CartItem
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

    cart = None
    ringkasan = {"total_item": 0, "total_harga": 0}

    # ===== USER LOGIN =====
    if id_user:
        uc = AmbilCartUseCase(
            CartRepositorySqlite(DB_PATH),
            CartItemRepositorySqlite(DB_PATH)
        )
        hasil = uc.execute(id_user=id_user)
        if hasil.is_success:
            cart = hasil.data
            update_cart_badge_from_cart(cart)

    # ===== GUEST =====
    else:
        guest_items = session.get("guest_cart", [])
        if guest_items:
            items = [
                CartItem(
                    id=f"guest-{i}",
                    id_cart="guest",
                    id_produk=item["id_produk"],
                    nama_produk=item["nama"],
                    harga_satuan=item["harga"],
                    jumlah=item["jumlah"]
                )
                for i, item in enumerate(guest_items)
            ]
            cart = Cart(id="guest", id_user="guest")
            cart.items = items
            update_cart_badge_from_guest()
        else:
            session["cart_total_items"] = 0

    # ===== RINGKASAN =====
    if cart and cart.items:
        ringkasan["total_item"] = sum(i.jumlah for i in cart.items)
        ringkasan["total_harga"] = sum(i.harga_satuan * i.jumlah for i in cart.items)

    return render_template("pages/cart/index.html", cart=cart, ringkasan=ringkasan)


# ===============================
# TAMBAH ITEM
# ===============================
@cart_bp.route("/tambah-item", methods=["POST"])
def tambah_item_cart():
    id_produk = request.form.get("id_produk")
    jumlah = int(request.form.get("jumlah", 1))

    produk = ProdukRepositorySqlite().get_by_id(id_produk)
    if not produk:
        flash("Produk tidak ditemukan", "error")
        return redirect(url_for("produk.daftar_produk"))

    # ===== GUEST =====
    if "user_id" not in session:
        guest_cart = session.get("guest_cart", [])

        for item in guest_cart:
            if item["id_produk"] == produk.id:
                item["jumlah"] += jumlah
                break
        else:
            guest_cart.append({
                "id_produk": produk.id,
                "nama": produk.nama,
                "harga": produk.harga,
                "jumlah": jumlah
            })

        session["guest_cart"] = guest_cart
        update_cart_badge_from_guest()

        flash("Item ditambahkan ke keranjang", "success")
        return redirect(url_for("cart.lihat_cart"))

    # ===== LOGIN =====
    uc = TambahItemCartUseCase(
        CartRepositorySqlite(DB_PATH),
        CartItemRepositorySqlite(DB_PATH),
        ProdukRepositorySqlite(),
        UUIDGeneratorService()
    )
    hasil = uc.execute(
        id_user=session["user_id"],
        id_produk=id_produk,
        jumlah=jumlah
    )

    flash(hasil.message, "success" if hasil.is_success else "error")
    return redirect(url_for("cart.lihat_cart"))


# ===============================
# UBAH JUMLAH
# ===============================
@cart_bp.route("/ubah-jumlah", methods=["POST"])
def ubah_jumlah_item():
    id_produk = int(request.form.get("id_produk"))
    jumlah = max(1, int(request.form.get("jumlah")))

    # ===== GUEST =====
    if "user_id" not in session:
        for item in session.get("guest_cart", []):
            if item["id_produk"] == id_produk:
                item["jumlah"] = jumlah
                break
        update_cart_badge_from_guest()
        return redirect(url_for("cart.lihat_cart"))

    # ===== LOGIN =====
    uc = UbahJumlahItemCartUseCase(
        CartItemRepositorySqlite(DB_PATH)
    )
    uc.execute(id_produk=id_produk, jumlah=jumlah)

    return redirect(url_for("cart.lihat_cart"))


# ===============================
# HAPUS ITEM
# ===============================
@cart_bp.route("/hapus-item/<int:id_produk>", methods=["POST"])
def hapus_item(id_produk):

    if "user_id" in session:
        uc = HapusItemCartUseCase(
            CartItemRepositorySqlite(DB_PATH)
        )
        uc.execute(id_item=id_produk)
    else:
        session["guest_cart"] = [
            i for i in session.get("guest_cart", [])
            if i["id_produk"] != id_produk
        ]
        update_cart_badge_from_guest()

    flash("Item berhasil dihapus", "success")
    return redirect(url_for("cart.lihat_cart"))


# ===============================
# KOSONGKAN CART
# ===============================
@cart_bp.route("/kosongkan", methods=["POST"])
def kosongkan_cart():

    if "user_id" in session:
        uc = KosongkanCartUseCase(
            CartRepositorySqlite(DB_PATH),
            CartItemRepositorySqlite(DB_PATH)
        )
        uc.execute(id_user=session["user_id"])
    else:
        session.pop("guest_cart", None)

    session["cart_total_items"] = 0
    session.modified = True

    flash("Keranjang berhasil dikosongkan", "success")
    return redirect(url_for("cart.lihat_cart"))

def update_cart_badge_from_cart(cart):
    if cart and cart.items:
        session["cart_total_items"] = len(cart.items)  # ✅ JUMLAH PRODUK
    else:
        session["cart_total_items"] = 0
    session.modified = True


def update_cart_badge_from_guest():
    guest_cart = session.get("guest_cart", [])
    session["cart_total_items"] = len(guest_cart)  # ✅ JUMLAH PRODUK
    session.modified = True

