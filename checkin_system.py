"""
checkin_system.py
Core logic for the Automated Check-In System (B2B Denim Events).

Designed as plain functions/classes so a future UI (Flask web app,
Tkinter desktop app, or a real QR scanner) can call directly into this
module without any rewrite.

Run as a CLI for now:
    python checkin_system.py
"""

import sqlite3
from datetime import datetime

from database import DB_NAME, get_connection


# ---------------------------------------------------------------------------
# 1. CORPORATE PROFILE GROUP DETECTION
# ---------------------------------------------------------------------------
# Keyword -> Group mapping. Checked against the company name first.
# If nothing matches confidently, we fall back to the registered_category
# field captured during registration.

GROUP_KEYWORDS = {
    "Mill / Manufacturer":  ["mill", "textile", "spinning", "weaving", "fabric"],
    "Chemical Supplier":    ["chemical", "dye", "finishing solutions"],
    "Retailer":             ["retail", "store", "mart"],
    "Brand":                ["brand", "fashion", "apparel", "jeans co", "wear"],
    "Buying House":         ["buying", "sourcing", "procurement"],
    "Trader":               ["trader", "trading", "import", "export"],
    "Garment Factory":      ["garment", "factory", "manufacturing unit"],
    "Press / Media":        ["press", "media", "magazine", "news"],
    "Speaker / Consultant":  ["consultant", "consulting", "advisory", "s.r.l", "studio"],
}


def detect_group_from_company(company_name: str) -> str | None:
    """Try to auto-detect the corporate group from the company name.
    Returns the group name, or None if no keyword matched."""
    name_lower = company_name.lower()
    for group, keywords in GROUP_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                return group
    return None


def resolve_corporate_group(company_name: str, registered_category: str) -> tuple[str, str]:
    """
    Resolve the visitor's corporate profile group.
    Returns (group, source) where source is 'auto-detected' or 'registered fallback'.
    """
    auto = detect_group_from_company(company_name)
    if auto:
        return auto, "auto-detected"
    return registered_category, "registered fallback"


# ---------------------------------------------------------------------------
# 2. LOOKUP — pulls registration details instantly by Visitor ID or phone
# ---------------------------------------------------------------------------

def find_visitor(identifier: str) -> dict | None:
    """
    Look up a visitor by Visitor ID or phone number.
    Returns a dict of visitor details, or None if not found.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT visitor_id, full_name, phone, company_name,
               registered_category, badge_type, checked_in, check_in_time
        FROM visitors
        WHERE visitor_id = ? OR phone = ?
    """, (identifier, identifier))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "visitor_id": row[0],
        "full_name": row[1],
        "phone": row[2],
        "company_name": row[3],
        "registered_category": row[4],
        "badge_type": row[5],
        "checked_in": bool(row[6]),
        "check_in_time": row[7],
    }


# ---------------------------------------------------------------------------
# 3. CHECK-IN ACTION — marks attendance + logs timestamp
# ---------------------------------------------------------------------------

def check_in_visitor(identifier: str) -> dict:
    """
    Full check-in flow:
      1. Look up the visitor's registration record.
      2. Resolve their corporate profile group.
      3. Mark them as checked in with a timestamp (if not already).
    Returns a result dict the UI/CLI can display.
    """
    visitor = find_visitor(identifier)

    if visitor is None:
        return {
            "status": "not_found",
            "message": f"No registration found for '{identifier}'. Please verify ID/phone."
        }

    group, source = resolve_corporate_group(
        visitor["company_name"], visitor["registered_category"]
    )

    if visitor["checked_in"]:
        return {
            "status": "already_checked_in",
            "visitor": visitor,
            "group": group,
            "group_source": source,
            "message": f"{visitor['full_name']} was already checked in at {visitor['check_in_time']}."
        }

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE visitors SET checked_in = 1, check_in_time = ?
        WHERE visitor_id = ?
    """, (now, visitor["visitor_id"]))
    conn.commit()
    conn.close()

    visitor["checked_in"] = True
    visitor["check_in_time"] = now

    return {
        "status": "success",
        "visitor": visitor,
        "group": group,
        "group_source": source,
        "message": f"Welcome {visitor['full_name']}! Checked in successfully."
    }


# ---------------------------------------------------------------------------
# 4. SIMPLE CLI (stand-in for the touchless entry kiosk / future UI)
# ---------------------------------------------------------------------------

def print_result(result: dict):
    print("-" * 50)
    if result["status"] == "not_found":
        print("❌", result["message"])
        print("-" * 50)
        return

    v = result["visitor"]
    print(f"✅ {result['message']}")
    print(f"Visitor ID     : {v['visitor_id']}")
    print(f"Name           : {v['full_name']}")
    print(f"Company        : {v['company_name']}")
    print(f"Badge Type     : {v['badge_type']}")
    print(f"Corporate Group: {result['group']}  ({result['group_source']})")
    print(f"Check-in Time  : {v['check_in_time']}")
    print("-" * 50)


def run_cli():
    print("=== Denimsandjeans Automated Check-In System ===")
    print("(Type 'exit' to quit)\n")

    while True:
        identifier = input("Enter Visitor ID or Phone Number: ").strip()
        if identifier.lower() == "exit":
            print("Session ended.")
            break
        if not identifier:
            continue

        result = check_in_visitor(identifier)
        print_result(result)
        print()


if __name__ == "__main__":
    run_cli()
