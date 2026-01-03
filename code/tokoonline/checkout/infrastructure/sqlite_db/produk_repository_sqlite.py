from katalog.domain.entities import Produk
from katalog.domain.repositories import ProdukRepository
from .db_settings import get_connection
from .mappers import produk_to_dict, produk_from_dict

class ProdukRepositorySqlite(ProdukRepository):
    def __init__(self):
        pass
        
    def add(self, produk: Produk) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "INSERT INTO produk (id, nama, deskripsi, harga, kode_barang) VALUES (?, ?, ?, ?, ?);"
        cursor.execute(sql, (produk.id, produk.nama, produk.deskripsi, produk.harga, produk.kode_barang))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()
        
    def update(self, produk: Produk) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "UPDATE produk SET id = ?, nama = ?, deskripsi = ?, harga = ?, kode_barang = ? WHERE id = ?;"
        cursor.execute(sql, (produk.id, produk.nama, produk.deskripsi, produk.harga, produk.kode_barang, produk.id))
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
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM produk WHERE 1 = 1 "
        params = []
        
        # filter nama
        if filter['nama']:
            sql += " AND nama LIKE ?"
            params.append(f"%{filter['nama']}%")
            
        # filter harga min
        if filter['harga_min']:
            sql += " AND harga > ?"
            params.append(filter['harga_min'])
        
        # filter harga max
        if filter['harga_max']:
            sql += " AND harga < ?"
            params.append(filter['harga_max'])
        
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [produk_from_dict(row) for row in rows]