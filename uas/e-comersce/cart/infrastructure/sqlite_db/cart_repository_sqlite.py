import sqlite3
import uuid
from cart.domain.entities import Cart, CartItem
from cart.domain.repositories import CartRepository, CartItemRepository
from .db_settings import DB_PATH

# ==========================================================
# CART REPOSITORY
# ==========================================================
class CartRepositorySqlite(CartRepository):

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ==========================
    # CART ITEM HANDLER
    # ==========================
    def add(self, id_cart, id_produk, nama_produk, harga_satuan, jumlah):
        conn = self._get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_cart_item, jumlah
            FROM cart_item
            WHERE id_cart = ? AND id_produk = ?
        """, (id_cart, id_produk))

        row = cur.fetchone()

        if row:
            cur.execute("""
                UPDATE cart_item
                SET jumlah = jumlah + ?
                WHERE id_cart_item = ?
            """, (jumlah, row["id_cart_item"]))
        else:
            cur.execute("""
                INSERT INTO cart_item (
                    id_cart_item, id_cart, id_produk,
                    nama_produk, harga_satuan, jumlah
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                id_cart,
                id_produk,
                nama_produk,
                harga_satuan,
                jumlah
            ))

        conn.commit()
        conn.close()

    # ==========================
    # CART CRUD
    # ==========================
    def create(self, cart: Cart):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cart (id, id_user) VALUES (?, ?)",
            (cart.id, cart.id_user)
        )
        conn.commit()
        conn.close()

    def update(self, cart: Cart):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE cart SET id_user=? WHERE id=?",
            (cart.id_user, cart.id)
        )
        conn.commit()
        conn.close()

    def delete_by_id(self, cart_id):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM cart WHERE id=?", (cart_id,))
        conn.commit()
        conn.close()

    def get_by_id(self, id_cart):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart WHERE id = ?", (id_cart,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        cart = Cart(id=row["id"], id_user=row["id_user"])
        cart.items = self.get_items(cart.id)
        return cart

    def get_all(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart")
        rows = cur.fetchall()
        conn.close()

        return [
            Cart(id=row["id"], id_user=row["id_user"])
            for row in rows
        ]

    def get_by_user(self, id_user):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart WHERE id_user = ?", (id_user,))
        rows = cur.fetchall()
        conn.close()

        carts = []
        for row in rows:
            cart = Cart(id=row["id"], id_user=row["id_user"])
            cart.items = self.get_items(cart.id)
            carts.append(cart)

        return carts

    def get_by_guest(self, guest_id):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM cart WHERE guest_id = ?",
            (guest_id,)
        )
        row = cur.fetchone()

        if not row:
            return None

        cart = Cart(
            id=row["id"],
            id_user=None
        )
        cart.items = self.get_items(cart.id)
        return cart

    def get_or_create_by_user(self, id_user):
        conn = self._get_conn()
        cur = conn.cursor()

        cur.execute("SELECT * FROM cart WHERE id_user = ?", (id_user,))
        row = cur.fetchone()

        if row:
            cart = Cart(id=row["id"], id_user=id_user)
            cart.items = self.get_items(cart.id)  # 🔥 PENTING
            conn.close()
            return cart

        cart_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO cart (id, id_user) VALUES (?, ?)",
            (cart_id, id_user)
        )
        conn.commit()
        conn.close()

        cart = Cart(id=cart_id, id_user=id_user)
        cart.items = []
        return cart


    # ==========================
    # CART ITEMS
    # ==========================
    def get_items(self, id_cart):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart_item WHERE id_cart = ?", (id_cart,))
        rows = cur.fetchall()
        conn.close()

        return [
            CartItem(
                id=row["id_cart_item"],
                id_cart=row["id_cart"],
                id_produk=row["id_produk"],
                nama_produk=row["nama_produk"],
                harga_satuan=row["harga_satuan"],
                jumlah=row["jumlah"]
            )
            for row in rows
        ]


# ==========================================================
# CART ITEM REPOSITORY
# ==========================================================
class CartItemRepositorySqlite(CartItemRepository):

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ==========================
    # ABSTRACT METHODS
    # ==========================
    def add(self, item: CartItem):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cart_item
            (id_cart_item, id_cart, id_produk, nama_produk, harga_satuan, jumlah)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item.id,
            item.id_cart,
            item.id_produk,
            item.nama_produk,
            item.harga_satuan,
            item.jumlah
        ))
        conn.commit()
        conn.close()

    def update(self, item: CartItem):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE cart_item
            SET jumlah = ?
            WHERE id_cart_item = ?
        """, (item.jumlah, item.id))
        conn.commit()
        conn.close()

    def delete_by_id(self, id_cart_item):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM cart_item WHERE id_cart_item = ?",
            (id_cart_item,)
        )
        conn.commit()
        conn.close()

    def get_by_id(self, id_cart_item):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM cart_item WHERE id_cart_item = ?",
            (id_cart_item,)
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return CartItem(
            id=row["id_cart_item"],
            id_cart=row["id_cart"],
            id_produk=row["id_produk"],
            nama_produk=row["nama_produk"],
            harga_satuan=row["harga_satuan"],
            jumlah=row["jumlah"]
        )

    def get_all(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart_item")
        rows = cur.fetchall()
        conn.close()

        return [
            CartItem(
                id=row["id_cart_item"],
                id_cart=row["id_cart"],
                id_produk=row["id_produk"],
                nama_produk=row["nama_produk"],
                harga_satuan=row["harga_satuan"],
                jumlah=row["jumlah"]
            )
            for row in rows
        ]

    # ==========================
    # CUSTOM METHODS
    # ==========================
    def get_by_cart(self, id_cart):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart_item WHERE id_cart = ?", (id_cart,))
        rows = cur.fetchall()
        conn.close()

        return [
            CartItem(
                id=row["id_cart_item"],
                id_cart=row["id_cart"],
                id_produk=row["id_produk"],
                nama_produk=row["nama_produk"],
                harga_satuan=row["harga_satuan"],
                jumlah=row["jumlah"]
            )
            for row in rows
        ]

    def get_by_cart_and_produk(self, id_cart, id_produk):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM cart_item
            WHERE id_cart = ? AND id_produk = ?
        """, (id_cart, id_produk))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return CartItem(
            id=row["id_cart_item"],
            id_cart=row["id_cart"],
            id_produk=row["id_produk"],
            nama_produk=row["nama_produk"],
            harga_satuan=row["harga_satuan"],
            jumlah=row["jumlah"]
        )
    
    def delete(self, item_id):
        """
        Menghapus item dari cart berdasarkan id_cart_item.
        Ini method yang dipanggil di use case checkout.
        """
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM cart_item WHERE id_cart_item = ?", (item_id,))
        conn.commit()
        conn.close()
    
    