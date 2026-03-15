import qrcode
import datetime
from flask import Blueprint, render_template, session
from db import db

qr_bp = Blueprint("qr", __name__)   # ✅ FIXED

@qr_bp.route("/create_qr")
def create_qr():

    login_time_str = session.get("admin_login_time")

    if not login_time_str:
        return "❌ Admin session expired. Please login again."

    login_time = datetime.datetime.fromisoformat(login_time_str)

    session_id = "SESSION_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # ✅ Expiry in UTC (for DB)
    expires_at = login_time + datetime.timedelta(minutes=10)

    db.sessions.insert_one({
        "session_id": session_id,
        "expires_at": expires_at   # ✅ Keep UTC in DB
    })

    img = qrcode.make(session_id)
    img.save("static/qr.png")

    # ✅ Convert UTC → IST for display
    ist_expires_at = expires_at + datetime.timedelta(hours=5, minutes=30)

    return render_template(
        "show_qr.html",
        session_id=session_id,
        expires_at=ist_expires_at   # ✅ Show IST
    )
