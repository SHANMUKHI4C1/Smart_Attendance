from flask import Blueprint, request
from datetime import datetime
from db import db
import pandas as pd
import matplotlib.pyplot as plt

attendance_bp = Blueprint("attendance", __name__)

# ✅ Helper → IST time
def get_ist_time():
    return datetime.utcnow().astimezone()

# ✅ GRAPH FUNCTION
def generate_graphs():

    records = list(db.attendance.find({}, {"_id": 0}))

    if not records:
        return

    df = pd.DataFrame(records)

    if df.empty:
        return

    counts = df["student"].value_counts()

    # ✅ Bar Chart
    plt.figure()
    counts.plot(kind="bar")
    plt.title("Attendance per Student")
    plt.xlabel("Students")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/bar_chart.png")
    plt.close()

    # ✅ Pie Chart
    plt.figure()
    counts.plot(kind="pie", autopct="%1.1f%%")
    plt.ylabel("")
    plt.title("Attendance Distribution")
    plt.tight_layout()
    plt.savefig("static/pie_chart.png")
    plt.close()


@attendance_bp.route("/mark_attendance", methods=["POST"])
def mark_attendance():

    student = request.form.get("student")
    session_id = request.form.get("session")

    if not student or not session_id:
        return "❌ Missing student or session"

    session = db.sessions.find_one({"session_id": session_id})

    if not session:
        return "❌ Invalid QR / Session"

    if datetime.utcnow() > session["expires_at"]:
        return "⏰ QR Expired"

    existing = db.attendance.find_one({
        "student": student,
        "session": session_id
    })

    if existing:
        return "⚠ Attendance Already Marked"

    ist_time = get_ist_time()

    db.attendance.insert_one({
        "student": student,
        "session": session_id,
        "time": ist_time,
        "time_str": ist_time.strftime("%Y-%m-%d %H:%M:%S")
    })

    # ✅ Auto update graphs
    generate_graphs()

    return "✅ Attendance Marked Successfully"
