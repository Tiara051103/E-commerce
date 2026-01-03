from katalog.domain.entities import VarianProduk
from .db_settings import get_connection

class VarianProdukRepositorySqlite:

    def add(self, produk_id, warna=None, ukuran=None, stok=0):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO varian_produk (produk_id, warna, ukuran, stok)
            VALUES (?, ?, ?, ?)
        """, (produk_id, warna, ukuran, stok))
        conn.commit()
        conn.close()

    def get_all_warna(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT warna
            FROM varian_produk
            WHERE warna IS NOT NULL
            AND TRIM(warna) != ''
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [row["warna"] for row in rows]


    def get_all_ukuran(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT ukuran
            FROM varian_produk
            WHERE ukuran IS NOT NULL
            AND TRIM(ukuran) != ''
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [row["ukuran"] for row in rows]

    
    def delete_by_produk(self, produk_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM varian_produk WHERE produk_id = ?;",
            (produk_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def get_by_produk(self, produk_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, produk_id, warna, ukuran, stok
            FROM varian_produk
            WHERE produk_id = ?
            """,
            (produk_id,)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            {
                "id": row["id"],
                "produk_id": row["produk_id"],
                "warna": row["warna"],
                "ukuran": row["ukuran"],
                "stok": row["stok"],
            }
            for row in rows
        ]

    def create(self, produk_id, warna, ukuran, stok):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO varian_produk (produk_id, warna, ukuran, stok)
            VALUES (?, ?, ?, ?)
        """, (produk_id, warna, ukuran, stok))

        conn.commit()
        conn.close()
