from flask import Blueprint, render_template, request, url_for, redirect, flash
from ..decorators import hx_required
from katalog.infrastructure.sqlite_db.kategori_repository_sqlite import (
    KategoriRepositorySqlite
)

from ..models import Produk
from katalog.application.use_cases import (
    DaftarProdukUseCase,
    CariProdukUseCase,
    FilterProdukUseCase,
    TambahProdukUseCase,
)
from katalog.infrastructure.sqlite_db.produk_repository_sqlite import (
    ProdukRepositorySqlite,
)
from katalog.infrastructure.sqlite_db.produk_kategori_repository_sqlite import (
    ProdukKategoriRepositorySqlite
)
from katalog.infrastructure.sqlite_db.brand_repository_sqlite import (
    BrandRepositorySqlite
)
from katalog.infrastructure.sqlite_db.varian_produk_repository_sqlite import (
    VarianProdukRepositorySqlite
)


from katalog.infrastructure.uuid.id_services import UuidGeneratorService

from ..utils import validasi
from ..dto import FilterProdukDTO


produk_bp = Blueprint("produk", __name__, url_prefix="/produk")


@produk_bp.route("/daftar-produk", methods=["GET"])
def daftar_produk():
    produk_repo = ProdukRepositorySqlite()
    kategori_repo = KategoriRepositorySqlite()
    brand_repo = BrandRepositorySqlite()
    varian_repo = VarianProdukRepositorySqlite()

    # =========================
    # DTO
    # =========================
    dto = FilterProdukDTO(**request.args)
    filter = dto.model_dump(exclude_none=True)

    context = {
        "params": dto.model_dump(),
        "kategori_list": kategori_repo.get_all(),
        "brand_list": brand_repo.get_all(),
        "warna_list": varian_repo.get_all_warna(),
        "ukuran_list": varian_repo.get_all_ukuran(),
        "daftar_produk": []
    }

    # =========================
    # DATA
    # =========================
    if filter:
        hasil = FilterProdukUseCase(produk_repo).execute(filter)
    else:
        hasil = DaftarProdukUseCase(produk_repo).execute()

    if hasil.is_success:
        context["daftar_produk"] = hasil.data

    # =========================
    # HTMX
    # =========================
    if request.headers.get("HX-Request") == "true":
        return render_template("partials/produk/daftar_produk.html", **context)

    return render_template("pages/produk/produk.html", **context)


@produk_bp.route("/cari-produk", methods=["GET"])
@hx_required
def cari_produk():
    keyword = request.args.get("keyword")

    produk_repository = ProdukRepositorySqlite()
    filter_produk_use_case = FilterProdukUseCase(produk_repository)
    filter = {"nama": keyword}
    hasil = filter_produk_use_case.execute(filter=filter)

    # cari_produk_use_case = CariProdukUseCase(produk_repository)
    # hasil = cari_produk_use_case.execute(keyword=keyword)
    if hasil.is_success:
        daftar_produk = hasil.data
    else:
        daftar_produk = []

    return render_template(
        "partials/produk/daftar_produk.html", daftar_produk=daftar_produk
    )
