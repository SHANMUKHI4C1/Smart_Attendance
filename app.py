import pandas as pd
from flask import Flask, send_file, render_template
from db import db
from attendance import generate_graphs

app = Flask(__name__)
app.secret_key = "attendance_secret"

# ✅ Import blueprints
from auth import auth_bp
from qr import qr_bp
from attendance import attendance_bp

# ✅ Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(qr_bp)
app.register_blueprint(attendance_bp)

# =========================
# ✅ EXPORT CSV ROUTE
# =========================
@app.route("/export_csv")
def export_csv():

    records = list(db.attendance.find({}, {"_id": 0}))

    if not records:
        return "No attendance data found"

    df = pd.DataFrame(records)
    csv_path = "attendance.csv"
    df.to_csv(csv_path, index=False)

    return send_file(csv_path, as_attachment=True)

# =========================
# ✅ MATLAB ANALYSIS PAGE
# =========================
@app.route("/analysis")
def analysis():
    generate_graphs()
    return render_template("analysis.html")

# =========================
# ✅ RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)
