from katalog.domain.entities import Produk
from katalog.domain.services import IdGeneratorService
from katalog.domain.repositories import ProdukRepository
from katalog.application.result import Result


class TambahProdukUseCase:
    def __init__(
        self,
        produk_repository: ProdukRepository,
        id_generator_service: IdGeneratorService,
    ):
        self.produk_repository = produk_repository
        self.id_generator_service = id_generator_service

    def execute(
        self, nama: str, deskripsi: str, harga: int, kode_barang: str
    ) -> Result:
        id = self.id_generator_service.generate_id()
        produk = Produk(
            id=id, nama=nama, deskripsi=deskripsi, harga=harga, kode_barang=kode_barang
        )
        hasil = self.produk_repository.add(produk)
        return Result.ok()


class UpdateProdukUseCase:
    def __init__(self, produk_repository: ProdukRepository):
        self.produk_repository = produk_repository

    def execute(
        self, id: str, nama: str, deskripsi: str, harga: int, kode_barang: str
    ) -> Result:
        produk = Produk(
            id=id, nama=nama, deskripsi=deskripsi, harga=harga, kode_barang=kode_barang
        )
        hasil = self.produk_repository.update(produk)
        return Result.ok()
    
class DeleteProdukUseCase:
    def __init__(self, produk_repository: ProdukRepository):
        self.produk_repository = produk_repository

    def execute(self, id: str) -> Result:
        hasil = self.produk_repository.delete_by_id(id)
        return Result.ok()


class DaftarProdukUseCase:
    def __init__(self, produk_repository: ProdukRepository):
        self.produk_repository = produk_repository

    def execute(self) -> Result:
        daftar_produk = self.produk_repository.get_all()
        return Result.ok(daftar_produk)


class DetailProdukUseCase:
    def __init__(self, produk_repository: ProdukRepository):
        self.produk_repository = produk_repository

    def execute(self, id: str) -> Result:
        produk = self.produk_repository.get_by_id(id)
        if produk is None:
            return Result.error("Produk tidak ditemukan")
        return Result.ok(produk)
    
class CariProdukUseCase:
    def __init__(self, produk_repository: ProdukRepository):
        self.produk_repository = produk_repository

    def execute(self, keyword: str) -> Result:
        daftar_produk = self.produk_repository.get_by_keyword(keyword)
        if daftar_produk is None:
            return Result.error("Produk tidak ditemukan")
        return Result.ok(daftar_produk)
    
class FilterProdukUseCase:
    def __init__(self, produk_repository: ProdukRepository):
        self.produk_repository = produk_repository

    def execute(self, filter: dict) -> Result:
        # validasi level aplikasi
        daftar_produk = self.produk_repository.get_by_filter(filter)
        if daftar_produk is None:
            return Result.error("Produk tidak ditemukan")
        return Result.ok(daftar_produk)
