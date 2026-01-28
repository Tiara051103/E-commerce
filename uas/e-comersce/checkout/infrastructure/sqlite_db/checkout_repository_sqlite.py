from checkout.domain.repositories import (
    CheckoutRepository,
    CheckoutItemRepository
)
from checkout.domain.entities import Checkout, CheckoutItem
from .db_settings import get_connection
from .mappers import (
    checkout_to_dict,
    checkout_from_dict,
    checkout_item_to_dict,
    checkout_item_from_dict
)


# ======================================================
# CHECKOUT REPOSITORY (HEADER)
# ======================================================
class CheckoutRepositorySqlite(CheckoutRepository):

    def create(self, checkout: Checkout) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO checkout (id, id_user, total_harga, status, created_at)
            VALUES (:id, :id_user, :total_harga, :status, :created_at)
            """,
            checkout_to_dict(checkout)
        )

        conn.commit()
        conn.close()

    def get_by_id(self, checkout_id: str) -> Checkout | None:
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(zip([d[0] for d in c.description], r))
        cur = conn.cursor()

        cur.execute("SELECT * FROM checkout WHERE id = ?", (checkout_id,))
        row = cur.fetchone()
        conn.close()

        if row is None:
            return None

        return checkout_from_dict(row)

    def get_by_user(self, id_user: int) -> list[Checkout]:
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(zip([d[0] for d in c.description], r))
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM checkout WHERE id_user = ? ORDER BY created_at DESC",
            (id_user,)
        )

        rows = cur.fetchall()
        conn.close()

        return [checkout_from_dict(row) for row in rows]

    def update_status(self, checkout_id: str, status: str) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE checkout SET status = ? WHERE id = ?",
            (status, checkout_id)
        )

        conn.commit()
        conn.close()

    def delete_by_checkout(self, checkout_id: str) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM checkout_item WHERE id_checkout = ?", (checkout_id,))
        cur.execute("DELETE FROM checkout WHERE id = ?", (checkout_id,))

        conn.commit()
        conn.close()

    def add_many(self, items: list[CheckoutItem]) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.executemany(
            """
            INSERT INTO checkout_item
            (id, id_checkout, id_produk, nama_produk, harga_satuan, jumlah, subtotal)
            VALUES (:id, :id_checkout, :id_produk, :nama_produk,
                    :harga_satuan, :jumlah, :subtotal)
            """,
            [checkout_item_to_dict(item) for item in items]
        )

        conn.commit()
        conn.close()


# ======================================================
# CHECKOUT ITEM REPOSITORY (DETAIL)
# ======================================================
class CheckoutItemRepositorySqlite(CheckoutItemRepository):

    def add(self, item: CheckoutItem) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO checkout_item
            (id, id_checkout, id_produk, nama_produk, harga_satuan, jumlah, subtotal)
            VALUES (:id, :id_checkout, :id_produk, :nama_produk,
                    :harga_satuan, :jumlah, :subtotal)
            """,
            checkout_item_to_dict(item)
        )

        conn.commit()
        conn.close()

    def get_by_checkout(self, checkout_id: str) -> list[CheckoutItem]:
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(zip([d[0] for d in c.description], r))
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM checkout_item WHERE id_checkout = ?",
            (checkout_id,)
        )

        rows = cur.fetchall()
        conn.close()

        return [checkout_item_from_dict(row) for row in rows]

    def add_many(self, items: list[CheckoutItem]) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.executemany(
            """
            INSERT INTO checkout_item
            (id, id_checkout, id_produk, nama_produk, harga_satuan, jumlah, subtotal)
            VALUES (:id, :id_checkout, :id_produk, :nama_produk,
                    :harga_satuan, :jumlah, :subtotal)
            """,
            [checkout_item_to_dict(item) for item in items]
        )
        conn.commit()
        conn.close()