import sqlite3
from cart.domain.entities import Cart, CartItem
from cart.domain.repositories import CartRepository, CartItemRepository
from .db_settings import DB_PATH


# =====================================================
# CART REPOSITORY SQLITE
# =====================================================
class CartRepositorySqlite(CartRepository):
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, cart: Cart):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cart (id_cart, id_user) VALUES (?, ?)",
            (cart.id, cart.id_user)
        )
        conn.commit()
        conn.close()

    def update(self, cart: Cart):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE cart SET id_user = ? WHERE id_cart = ?",
            (cart.id_user, cart.id)
        )
        conn.commit()
        conn.close()

    def delete_by_id(self, id: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM cart WHERE id_cart = ?", (id,))
        conn.commit()
        conn.close()

    def get_all(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart")
        rows = cur.fetchall()
        conn.close()

        return [
            Cart(id=row["id_cart"], id_user=row["id_user"])
            for row in rows
        ]

    def get_by_id(self, id: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart WHERE id_cart = ?", (id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return Cart(id=row["id_cart"], id_user=row["id_user"])

    def get_by_user(self, id_user: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM cart WHERE id_user = ? AND id_cart IS NOT NULL",
            (id_user,)
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return Cart(id=row["id_cart"], id_user=row["id_user"])


# =====================================================
# CART ITEM REPOSITORY SQLITE
# =====================================================
class CartItemRepositorySqlite(CartItemRepository):

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, item: CartItem):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO cart_item
            (id_cart_item, id_cart, id_produk, nama_produk, harga_satuan, jumlah)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item.id,
                item.id_cart,
                item.id_produk,
                item.nama_produk,
                item.harga_satuan,
                item.jumlah
            )
        )
        conn.commit()
        conn.close()

    def update(self, item: CartItem):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE cart_item SET jumlah = ? WHERE id_cart_item = ?",
            (item.jumlah, item.id)
        )
        conn.commit()
        conn.close()

    def delete_by_id(self, id: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM cart_item WHERE id_cart_item = ?", (id,))
        conn.commit()
        conn.close()

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


    def get_by_id(self, id: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cart_item WHERE id_cart_item = ?", (id,))
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

    def get_by_cart(self, id_cart: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM cart_item WHERE id_cart = ?",
            (id_cart,)
        )
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


    def get_by_cart_and_produk(self, id_cart: str, id_produk: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM cart_item
            WHERE id_cart = ? AND id_produk = ?
            """,
            (id_cart, id_produk)
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

