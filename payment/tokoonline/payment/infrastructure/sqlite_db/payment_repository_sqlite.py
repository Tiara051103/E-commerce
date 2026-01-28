# payment/infrastructure/sqlite_db/payment_repository_sqlite.py
from payment.domain.repositories import PaymentRepository
from payment.domain.entities import Payment
from .db_settings import get_connection
from .mappers import payment_to_dict, payment_from_dict


class PaymentRepositorySqlite(PaymentRepository):

    def create(self, payment: Payment) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO payment
            (id, id_checkout, id_user, metode, total_harga,
             status, created_at, paid_at)
            VALUES
            (:id, :id_checkout, :id_user, :metode, :total_harga,
             :status, :created_at, :paid_at)
            """,
            payment_to_dict(payment)
        )

        conn.commit()
        conn.close()

    def get_by_id(self, payment_id: str):
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(zip([d[0] for d in c.description], r))
        cur = conn.cursor()

        cur.execute("SELECT * FROM payment WHERE id = ?", (payment_id,))
        row = cur.fetchone()
        conn.close()

        return payment_from_dict(row) if row else None

    def get_by_checkout(self, id_checkout: str):
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(zip([d[0] for d in c.description], r))
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM payment WHERE id_checkout = ?",
            (id_checkout,)
        )

        row = cur.fetchone()
        conn.close()

        return payment_from_dict(row) if row else None

    def get_by_user(self, id_user: int):
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(zip([d[0] for d in c.description], r))
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM payment WHERE id_user = ? ORDER BY created_at DESC",
            (id_user,)
        )

        rows = cur.fetchall()
        conn.close()

        return [payment_from_dict(row) for row in rows]

    def update_status(self, payment_id: str, status: str) -> None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE payment
            SET status = ?, paid_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (status, payment_id)
        )

        conn.commit()
        conn.close()
