"""
app.py
Web UI (kiosk screen) for the Denimsandjeans Automated Check-In System.

Run with:
    python3 app.py

Then open http://localhost:5000 in a browser.
Make sure you've already run `python3 database.py` once to create checkin.db.
"""

from flask import Flask, render_template, request
from checkin_system import check_in_visitor
from company_verifier import verify_company_denim_relation
from database import create_tables, seed_data
import os

app = Flask(__name__)

# Make sure the database exists and has sample data when the app starts
# (important on a fresh deploy where no one has run database.py manually)
if not os.path.exists("checkin.db"):
    create_tables()
    seed_data()


@app.route("/", methods=["GET", "POST"])
def kiosk():
    result = None
    submitted_value = ""
    company_result = None
    submitted_company = ""

    if request.method == "POST":
        form_name = request.form.get("form_name")

        if form_name == "checkin":
            submitted_value = request.form.get("identifier", "").strip()
            if submitted_value:
                result = check_in_visitor(submitted_value)

        elif form_name == "verify_company":
            submitted_company = request.form.get("company_name", "").strip()
            if submitted_company:
                company_result = verify_company_denim_relation(submitted_company)

    return render_template(
        "kiosk.html",
        result=result,
        submitted_value=submitted_value,
        company_result=company_result,
        submitted_company=submitted_company,
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
