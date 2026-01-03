from katalog.domain.entities import Brand
from .db_settings import get_connection

class BrandRepositorySqlite:
    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nama FROM brand;")
        rows = cur.fetchall()
        conn.close()
        return [Brand(id=row["id"], nama=row["nama"]) for row in rows]

    def get_or_create(self, nama: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nama FROM brand WHERE LOWER (nama) = LOWER (?);", (nama,))
        row = cur.fetchone()
        if row:
            return Brand(id=row["id"], nama=row["nama"])
        cur.execute("INSERT INTO brand (nama) VALUES (?);",(nama.strip(),) )
        brand_id = cur.lastrowid
        conn.commit()
        conn.close()
        return Brand(id=brand_id, nama=nama)

    def get_by_nama(self, nama):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nama FROM brand WHERE nama = ?",
            (nama,)
        )
        row = cur.fetchone()
        conn.close()

        if row:
            return Brand(id=row["id"], nama=row["nama"])
        return None

    def create(self, nama):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO brand (nama) VALUES (?)",
            (nama,)
        )
        conn.commit()
        brand_id = cur.lastrowid
        conn.close()

        return Brand(id=brand_id, nama=nama)
