from flask import Blueprint, render_template, request, url_for, redirect, flash, session

from auth.application.use_cases import LoginUserUseCase, RegisterUserUseCase, CheckUserUseCase
from auth.infrastructure.sqlite_db.repositories import UserRepositorySQLite
from auth.infrastructure.services import PasswordService, IdGeneratorService

from ..dto import UserRegisterRequestDTO, UserLoginRequestDTO

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        user_repository = UserRepositorySQLite()
        cek_user_use_case = CheckUserUseCase(user_repository=user_repository)
        hasil = cek_user_use_case.execute(session["user_id"])
        if not hasil.is_success:
            return redirect(url_for("auth.login"))
        return redirect(url_for("auth.dashboard"))
    
    context = {}
    
    if request.method == "POST":
        form_data = UserRegisterRequestDTO(**request.form)
        user = form_data.model_dump()
        user_repository = UserRepositorySQLite()
        id_service = IdGeneratorService()
        password_service = PasswordService()
        register_user_use_case = RegisterUserUseCase(user_repository, id_service, password_service)
        hasil = register_user_use_case.execute(**user)
        if hasil.is_success:
            flash("User berhasil didaftarkan", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("User gagal didaftarkan", "error")
            return redirect(url_for("auth.register"))

    return render_template("pages/auth/register.html", **context)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        user_repository = UserRepositorySQLite()
        cek_user_use_case = CheckUserUseCase(user_repository=user_repository)
        hasil = cek_user_use_case.execute(session["user_id"])
        if not hasil.is_success:
            return redirect(url_for("auth.login"))
        return redirect(url_for("auth.dashboard"))
    context = {}
    
    if request.method == "POST":
        form_data = UserLoginRequestDTO(**request.form)
        user = form_data.model_dump()
        user_repository = UserRepositorySQLite()
        password_service = PasswordService()
        login_user_use_case = LoginUserUseCase(user_repository=user_repository, password_service=password_service)
        hasil = login_user_use_case.execute(**user)
        if hasil.is_success:
            session["user_id"] = hasil.data.id
            flash("User berhasil login", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("User gagal login", "error")
            flash(hasil.error, "error")
            return redirect(url_for("auth.login"))

    return render_template("pages/auth/login.html", **context)

@auth_bp.route("/logout", methods=["GET"])
def logout():
    # hapus session login
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
    
@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user_repository = UserRepositorySQLite()
        cek_user_use_case = CheckUserUseCase(user_repository=user_repository)
        hasil = cek_user_use_case.execute(session["user_id"])
        if hasil.is_success:
            return render_template("pages/auth/dashboard.html")
        return redirect(url_for("auth.dashboard"))
    else:
        return redirect(url_for("auth.login"))
    
    