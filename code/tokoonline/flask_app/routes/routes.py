import os, uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from katalog.application.use_cases import (
    TambahProdukUseCase, DaftarProdukUseCase, DetailProdukUseCase, 
    UpdateProdukUseCase, DeleteProdukUseCase, CariProdukUseCase,
    FilterProdukUseCase, )
from katalog.infrastructure.sqlite_db.produk_repository_sqlite import ( 
    ProdukRepositorySqlite )
from katalog.infrastructure.sqlite_db.kategori_repository_sqlite import (
    KategoriRepositorySqlite)
from katalog.infrastructure.uuid.id_services import UuidGeneratorService
from ..models import Produk
from katalog.domain.entities import Produk, Kategori
from katalog.infrastructure.sqlite_db.produk_kategori_repository_sqlite import (
    ProdukKategoriRepositorySqlite
)
from katalog.infrastructure.sqlite_db.brand_repository_sqlite import (
    BrandRepositorySqlite
)
from katalog.infrastructure.sqlite_db.varian_produk_repository_sqlite import (
    VarianProdukRepositorySqlite
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = "flask_app/static/uploads/produk"

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    context = {}

    return render_template("pages/index.html", **context)

@main_bp.route("/produk", methods=["GET", "POST"])
def produk():
    produk_repo = ProdukRepositorySqlite()
    kategori_repo = KategoriRepositorySqlite()
    produk_kategori_repo = ProdukKategoriRepositorySqlite()
    varian_repo = VarianProdukRepositorySqlite()
    brand_repo = BrandRepositorySqlite()
    id_service = UuidGeneratorService()

    # =========================
    # FILTER (GET)
    # =========================
    filter_data = {
        "nama": request.args.get("nama"),
        "brand": request.args.get("brand"),
        "warna": request.args.get("warna"),
        "ukuran": request.args.get("ukuran"),
        "stok_min": request.args.get("stok_min"),
        "harga_min": request.args.get("harga_min"),
        "harga_max": request.args.get("harga_max"),
        "kategori_id": request.args.get("kategori_id"),
    }

    # buang value kosong
    filter_data = {k: v for k, v in filter_data.items() if v}

    if filter_data:
        hasil = FilterProdukUseCase(produk_repo).execute(filter_data)
    else:
        hasil = DaftarProdukUseCase(produk_repo).execute()

    context = {
        "daftar_produk": hasil.data if hasil.is_success else [],
        "kategori_list": kategori_repo.get_all(),
        "brand_list": brand_repo.get_all(),
        "warna_list": varian_repo.get_all_warna(),
        "ukuran_list": varian_repo.get_all_ukuran(),
        "params": filter_data,
    }

    # =========================
    # TAMBAH PRODUK (POST)
    # =========================
    if request.method == "POST":
        # ===== GAMBAR =====
        gambar = request.files.get("gambar")
        nama_file = None
        if gambar and gambar.filename:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            nama_file = secure_filename(gambar.filename)
            gambar.save(os.path.join(UPLOAD_FOLDER, nama_file))

        # ===== KATEGORI =====
        kategori_baru = request.form.get("kategori_baru", "").strip()
        kategori_id = request.form.get("kategori_id")

        if kategori_baru:
            kategori = kategori_repo.get_or_create(kategori_baru)
            kategori_id = kategori.id
        elif kategori_id:
            kategori_id = int(kategori_id)
        else:
            flash("Kategori wajib diisi", "error")
            return redirect(url_for("main.produk"))

        # ===== BRAND =====
        brand_baru = request.form.get("brand_baru", "").strip()
        brand_id = request.form.get("brand_id")

        if brand_baru:
            brand = brand_repo.get_by_nama(brand_baru)
            if not brand:
                brand = brand_repo.create(brand_baru)
            brand_id = brand.id
        elif brand_id:
            brand_id = int(brand_id)
        else:
            flash("Brand wajib diisi", "error")
            return redirect(url_for("main.produk"))

       # ===== VARIAN (FIX + NORMALISASI) =====
        warna_list = request.form.getlist("warna[]")
        ukuran_list = request.form.getlist("ukuran[]")
        stok_list = request.form.getlist("stok[]")

        varians = []
        for w, u, s in zip(warna_list, ukuran_list, stok_list):
            if not w and not u:
                continue

            warna = w.strip().title()     # 🔥 Hitam, Merah, Biru
            ukuran = u.strip().upper()    # 🔥 S, M, L, XL

            varians.append({
                "warna": warna,
                "ukuran": ukuran,
                "stok": int(s) if s else 0,
            })

        if not varians:
            flash("Minimal 1 varian harus diisi", "error")
            return redirect(url_for("main.produk"))

        # ===== SIMPAN =====
        use_case = TambahProdukUseCase(
            produk_repo, varian_repo, brand_repo, id_service
        )

        hasil_tambah = use_case.execute(
            nama=request.form["nama"],
            deskripsi=request.form["deskripsi"],
            harga=int(request.form["harga"]),
            kode_barang=request.form["kode_barang"],
            gambar=nama_file,
            brand_id=brand_id,
            varians=varians,
        )

        if hasil_tambah.is_success:
            produk_kategori_repo.add(hasil_tambah.data.id, kategori_id)
            flash("Produk berhasil ditambahkan", "success")
        else:
            flash("Produk gagal ditambahkan", "error")

        return redirect(url_for("main.produk"))

    return render_template("pages/produk/produk.html", **context)

@main_bp.route("/hapus-produk/<id>", methods=["POST"])
def hapus_produk(id):
    produk_repo = ProdukRepositorySqlite()
    produk_kategori_repo = ProdukKategoriRepositorySqlite()
    varian_repo = VarianProdukRepositorySqlite()
    

    # =========================
    # AMBIL DATA PRODUK
    # =========================
    detail_use_case = DetailProdukUseCase(produk_repo)
    hasil_detail = detail_use_case.execute(id)

    if not hasil_detail.is_success:
        flash("Produk tidak ditemukan", "error")
        return redirect(url_for("main.produk"))

    produk = hasil_detail.data

    # =========================
    # HAPUS FILE GAMBAR
    # =========================
    if produk.gambar:
        path_gambar = os.path.join(UPLOAD_FOLDER, produk.gambar)
        if os.path.exists(path_gambar):
            os.remove(path_gambar)

    # =========================
    # 🔥 HAPUS RELASI (WAJIB)
    # =========================
    varian_repo.delete_by_produk_id(id)
    produk_kategori_repo.delete_by_produk_id(id)

    # =========================
    # HAPUS PRODUK
    # =========================
    hapus_use_case = DeleteProdukUseCase(produk_repo)
    hasil = hapus_use_case.execute(id=id)

    flash(
        "Produk berhasil dihapus" if hasil.is_success else "Produk gagal dihapus",
        "success" if hasil.is_success else "error"
    )

    return redirect(url_for("main.produk"))

@main_bp.route("/produk/<int:id>", methods=["GET", "POST"])
def detail_produk(id):
    produk_repo = ProdukRepositorySqlite()
    kategori_repo = KategoriRepositorySqlite()
    produk_kategori_repo = ProdukKategoriRepositorySqlite()
    varian_repo = VarianProdukRepositorySqlite()
    brand_repo = BrandRepositorySqlite()

    hasil = DetailProdukUseCase(produk_repo).execute(id)
    if not hasil.is_success:
        return "Produk tidak ditemukan", 404

    produk = hasil.data

    if request.method == "POST":
        # ===== GAMBAR =====
        gambar_file = request.files.get("gambar")
        nama_file = produk.gambar

        if gambar_file and gambar_file.filename:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            nama_file = secure_filename(gambar_file.filename)
            gambar_file.save(os.path.join(UPLOAD_FOLDER, nama_file))

        # ===== VARIAN =====
        warna_list = request.form.getlist("warna[]")
        ukuran_list = request.form.getlist("ukuran[]")
        stok_list = request.form.getlist("stok[]")

        varians = []
        for w, u, s in zip(warna_list, ukuran_list, stok_list):
            if not w and not u:
                continue

            varians.append({
                "warna": w.strip().title(),
                "ukuran": u.strip().upper(),
                "stok": int(s) if s else 0,
            })

        if not varians:
            flash("Minimal 1 varian harus diisi", "error")
            return redirect(url_for("main.detail_produk", id=id))

        # ===== BRAND =====
        # ===== BRAND (FIX FINAL) =====
        brand_baru = request.form.get("brand_baru", "").strip()
        brand_id = request.form.get("brand_id")

        if brand_baru:
            brand = brand_repo.get_by_nama(brand_baru)
            if not brand:
                brand = brand_repo.create(brand_baru)
            brand_id = brand.id
        elif brand_id:
            brand_id = int(brand_id)
        else:
            flash("Brand wajib diisi", "error")
            return redirect(url_for("main.detail_produk", id=id))
        # ===== UPDATE PRODUK =====
        UpdateProdukUseCase(produk_repo, varian_repo).execute(
            id=id,
            nama=request.form["nama"],
            deskripsi=request.form["deskripsi"],
            harga=int(request.form["harga"]),
            kode_barang=request.form["kode_barang"],
            gambar=nama_file,
            brand_id=brand_id,
            varians=varians,
        )

        # ===== KATEGORI =====
        produk_kategori_repo.delete_by_produk_id(id)
        for kategori_id in request.form.getlist("kategori_ids"):
            produk_kategori_repo.add(id, kategori_id)

        flash("Produk berhasil diupdate", "success")
        return redirect(url_for("main.detail_produk", id=id))

    context = {
        "produk": produk,
        "kategori_list": kategori_repo.get_all(),
        "kategori_produk": produk_kategori_repo.get_kategori_ids_by_produk(id),
        "brand_list": brand_repo.get_all(),
        "varians": varian_repo.get_by_produk(id),
    }

    if request.headers.get("HX-Request") == "true":
        return render_template("partials/produk/detail_produk.html", **context)

    return render_template("partials/produk/detail_produk.html", **context)

@main_bp.route("/cari-produk", methods=["GET"])
def cari_produk():
    context = {"produk": None}
    
    keyword = request.args.get("keyword")

    produk_repository = ProdukRepositorySqlite()
    cari_produk_use_case = CariProdukUseCase(produk_repository)
    hasil = cari_produk_use_case.execute(keyword=keyword)
    if hasil.is_success:
        context["produk"] = hasil.data

    return render_template("pages/cari_produk.html", **context)
