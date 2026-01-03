from katalog.domain.entities import Kategori
from katalog.domain.repositories import KategoriRepository
from .db_settings import get_connection


class KategoriRepositorySqlite(KategoriRepository):
    def __init__(self):
        pass

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nama FROM kategori;")
        rows = cur.fetchall()
        conn.close()

        return [Kategori(id=row["id"], nama=row["nama"]) for row in rows]

    def add(self, kategori: Kategori):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO kategori (nama) VALUES (?);",
            (kategori.nama,)
        )

        conn.commit()
        conn.close()

    def update(self, kategori: Kategori) -> None:
        conn = get_connection()
        cur = conn.cursor()

        sql = "UPDATE kategori SET nama = ? WHERE id = ?;"
        cur.execute(sql, (kategori.nama, kategori.id))

        conn.commit()
        cur.close()
        conn.close()

    def delete_by_id(self, id) -> None:
        conn = get_connection()
        cur = conn.cursor()

        sql = "DELETE FROM kategori WHERE id = ?;"
        cur.execute(sql, (id,))

        conn.commit()
        cur.close()
        conn.close()

    def get_by_id(self, id) -> Kategori | None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, nama FROM kategori WHERE id = ?;", (id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return Kategori(
                id=row["id"],
                nama=row["nama"]
            )
        return None
    
    def get_by_nama(self, nama: str) -> Kategori | None:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, nama FROM kategori WHERE nama = ?;",
            (nama,)
        )
        row = cur.fetchone()

        conn.close()

        if row:
            return Kategori(id=row["id"], nama=row["nama"])
        return None

    def get_or_create(self, nama: str) -> Kategori:
        kategori = self.get_by_nama(nama)

        if kategori:
            return kategori

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO kategori (nama) VALUES (?);",
            (nama,)
        )
        kategori_id = cur.lastrowid
        conn.commit()
        conn.close()

        return Kategori(id=kategori_id, nama=nama)
