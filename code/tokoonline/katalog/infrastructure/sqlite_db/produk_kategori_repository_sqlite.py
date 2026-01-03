from .db_settings import get_connection
class ProdukKategoriRepositorySqlite:

    def add(self, produk_id: str, kategori_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO produk_kategori (produk_id, kategori_id)
            VALUES (?, ?)
            """,
            (produk_id, kategori_id)
        )
        conn.commit()
        conn.close()

    def delete_by_produk_id(self, produk_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM produk_kategori WHERE produk_id = ?",
            (produk_id,)
        )
        conn.commit()
        conn.close()
        
    def get_kategori_ids_by_produk(self, produk_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT kategori_id
            FROM produk_kategori
            WHERE produk_id = ?
        """, (produk_id,))

        rows = cursor.fetchall()
        conn.close()

        return [row["kategori_id"] for row in rows]
