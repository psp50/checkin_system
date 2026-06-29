"""
database.py
Sets up the SQLite database for the Denimsandjeans Automated Check-In System
and seeds it with sample visitor registration data.

Run this once before using checkin_system.py:
    python database.py
"""

import sqlite3

DB_NAME = "checkin.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            visitor_id      TEXT PRIMARY KEY,
            full_name       TEXT NOT NULL,
            phone           TEXT NOT NULL,
            company_name    TEXT NOT NULL,
            registered_category TEXT NOT NULL,   -- filled at registration (fallback)
            badge_type      TEXT NOT NULL,        -- Visitor / Exhibitor / Speaker / Press
            checked_in      INTEGER DEFAULT 0,    -- 0 = not checked in, 1 = checked in
            check_in_time   TEXT
        )
    """)

    conn.commit()
    conn.close()


def seed_data():
    sample_visitors = [
        # visitor_id, full_name, phone, company_name, registered_category, badge_type
        ("DJ001", "Arjun Mehta",     "9876500001", "Vardhman Textiles Ltd",        "Mill",          "Exhibitor"),
        ("DJ002", "Sara Lopez",      "9876500002", "Zara Retail Group",            "Retailer",      "Visitor"),
        ("DJ003", "Kenji Watanabe",  "9876500003", "Tokyo Denim Sourcing Co",       "Buying House",  "Visitor"),
        ("DJ004", "Fatima Al-Sayed", "9876500004", "Cairo Garment Traders",         "Trader",        "Visitor"),
        ("DJ005", "Hannah Kim",      "9876500005", "Seoul Fashion Brands Inc",      "Brand",         "Visitor"),
        ("DJ006", "Marco Rossi",     "9876500006", "Rossi Chemical Solutions",      "Chemical Supplier", "Exhibitor"),
        ("DJ007", "Priya Nair",      "9876500007", "DenimWorks Garment Factory",    "Garment Factory", "Exhibitor"),
        ("DJ008", "David Tring",     "9876500008", "Independent Consultant",        "Speaker",       "Speaker"),
        ("DJ009", "Lucia Rosin",     "9876500009", "MEIDEA s.r.l.",                 "Speaker",       "Speaker"),
        ("DJ010", "Riya Sharma",     "9876500010", "Fashion Press Network",         "Press",         "Press"),
    ]

    conn = get_connection()
    cur = conn.cursor()
    cur.executemany("""
        INSERT OR IGNORE INTO visitors
        (visitor_id, full_name, phone, company_name, registered_category, badge_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_visitors)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    seed_data()
    print(f"Database '{DB_NAME}' created and seeded with sample visitors.")
