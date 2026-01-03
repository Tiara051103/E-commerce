from katalog.domain.entities import Produk, Kategori
from katalog.domain.repositories import ProdukRepository
from .db_settings import get_connection
from .mappers import produk_to_dict, produk_from_dict

class ProdukRepositorySqlite(ProdukRepository):
    def __init__(self):
        pass
        
    def add(self, produk: Produk) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "INSERT INTO produk (nama, deskripsi, harga, kode_barang, gambar, brand_id) VALUES (?, ?, ?, ?, ?, ?);"
        cursor.execute(sql, (produk.nama, produk.deskripsi, produk.harga, produk.kode_barang, produk.gambar, produk.brand_id))

        koneksi.commit()
        produk_id = cursor.lastrowid
       
        produk.id = produk_id
        cursor.close()
        koneksi.close()
        
    def update(self, produk: Produk) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        sql = """
        UPDATE produk
        SET nama = ?, deskripsi = ?, harga = ?, kode_barang = ?, gambar = ?, brand_id = ?
        WHERE id = ?;
        """

        cursor.execute(sql, (
            produk.nama,
            produk.deskripsi,
            produk.harga,
            produk.kode_barang,
            produk.gambar,
            produk.brand_id,
            produk.id
        ))

        koneksi.commit()
        cursor.close()
        koneksi.close()

        
    def delete_by_id(self, id) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "DELETE FROM produk WHERE id = ?;"
        cursor.execute(sql, (id,))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()
        
    def delete_by_produk_id(self, produk_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM produk_kategori WHERE produk_id = ?;",
            (produk_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def get_all(self) -> list[Produk]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM produk;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [produk_from_dict(row) for row in rows]
    
    def get_by_id(self, id) -> Produk:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM produk WHERE id = ?;"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return produk_from_dict(row)
    
    def get_by_nama(self, nama):
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM produk WHERE nama = ?;"
        cursor.execute(sql, (nama,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return produk_from_dict(row)
    
    def get_by_keyword(self, keyword) -> list[Produk]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM produk WHERE nama LIKE ?;"
        cursor.execute(sql, (f"%{keyword}%",))
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [produk_from_dict(row) for row in rows]
    
    def get_by_filter(self, filter: dict) -> list[Produk]:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT DISTINCT p.*
        FROM produk p
        """

        params = []

        if filter.get("warna") or filter.get("ukuran") or filter.get("stok_min"):
            sql += " JOIN varian_produk v ON v.produk_id = p.id "

        if filter.get("kategori_id"):
            sql += " JOIN produk_kategori pk ON pk.produk_id = p.id "

        # ===== WHERE =====
        sql += " WHERE 1=1 "

        if filter.get("brand_id"):
            sql += " AND p.brand_id = ? "
            params.append(int(filter["brand_id"]))

        if filter.get("warna"):
            sql += " AND LOWER(v.warna) = LOWER(?) "
            params.append(filter["warna"])

        if filter.get("ukuran"):
            sql += " AND LOWER(v.ukuran) = LOWER(?) "
            params.append(filter["ukuran"])

        if filter.get("stok_min"):
            sql += " AND v.stok >= ? "
            params.append(int(filter["stok_min"]))

        if filter.get("nama"):
            sql += " AND p.nama LIKE ? "
            params.append(f"%{filter['nama']}%")

        if filter.get("kategori_id"):
            sql += " AND pk.kategori_id = ? "
            params.append(int(filter["kategori_id"]))

        if filter.get("harga_min"):
            sql += " AND p.harga >= ? "
            params.append(int(filter["harga_min"]))

        if filter.get("harga_max"):
            sql += " AND p.harga <= ? "
            params.append(int(filter["harga_max"]))

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [produk_from_dict(row) for row in rows]
