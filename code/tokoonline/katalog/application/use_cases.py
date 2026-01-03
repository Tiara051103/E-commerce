from katalog.domain.entities import Produk
from katalog.domain.services import IdGeneratorService
from katalog.domain.repositories import ProdukRepository
from katalog.application.result import Result


class TambahProdukUseCase:
    def __init__(self, produk_repo, varian_repo, brand_repo, id_service):
        self.produk_repo = produk_repo
        self.varian_repo = varian_repo
        self.brand_repo = brand_repo
        self.id_service = id_service

    def execute(
        self,
        nama: str,
        deskripsi: str,
        harga: int,
        kode_barang: str,
        gambar: str | None,
        brand_id: int,
        varians: list[dict],
    ):
        try:
            produk = Produk(
                id=None,
                nama=nama,
                deskripsi=deskripsi,
                harga=harga,
                kode_barang=kode_barang,
                gambar=gambar,
                brand_id=brand_id,  # 🔥 SIMPAN ID
            )

            self.produk_repo.add(produk)

            for v in varians:
                self.varian_repo.add(
                    produk_id=produk.id,
                    warna=v["warna"],
                    ukuran=v["ukuran"],
                    stok=v["stok"],
                )

            return Result(is_success=True, data=produk)

        except Exception as e:
            return Result(is_success=False, error=str(e))

class UpdateProdukUseCase:

    def __init__(self, produk_repo, varian_repo):
        self.produk_repo = produk_repo
        self.varian_repo = varian_repo

    def execute(
        self,
        id,
        nama,
        deskripsi,
        harga,
        kode_barang,
        gambar,
        brand_id,
        varians
    ):
        # =========================
        # UPDATE PRODUK
        # =========================
        produk = Produk(
            id=id,
            nama=nama,
            deskripsi=deskripsi,
            harga=harga,
            kode_barang=kode_barang,
            gambar=gambar,
            brand_id=brand_id
        )

        self.produk_repo.update(produk)

        # =========================
        # UPDATE VARIAN
        # =========================
        self.varian_repo.delete_by_produk(id)

        for v in varians:
            self.varian_repo.create(
                produk_id=id,
                warna=v["warna"],
                ukuran=v["ukuran"],
                stok=v["stok"]
            )

        return True

    
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
