from flask import Blueprint, render_template, request, redirect
import bcrypt
from db import db
from flask import session
import datetime

auth_bp = Blueprint("auth", __name__)   # ✅ FIXED

ADMIN_ID = "admin123"
ADMIN_PASS = "admin@123"

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == ADMIN_ID and pwd == ADMIN_PASS:
            session["admin_login_time"] = datetime.datetime.utcnow().isoformat()
            return redirect("/admin")

        u = db.users.find_one({"username": user})
        if u and bcrypt.checkpw(pwd.encode(), u["password"]):
            return redirect("/student")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pwd = bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt())

        db.users.insert_one({
            "username": user,
            "password": pwd,
            "role": "student"
        })
        return redirect("/")
    return render_template("register.html")

# ✅ ADD THESE BELOW

@auth_bp.route("/student")
def student_dashboard():
    return render_template("student.html")

@auth_bp.route("/admin")
def admin_dashboard():
    return render_template("admin.html")
