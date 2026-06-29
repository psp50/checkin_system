# Denimsandjeans — Automated Check-In System

A simple web page for checking people in at the show entrance, and a second
tool that checks whether a company is connected to the denim/textile
industry before letting them in.

This README explains everything in plain language — no tech background needed.

---

## What this actually does

Think of it as a digital reception desk for the show:

1. **Check-In Box** — Someone gives their Visitor ID (like `DJ001`) or their
   phone number. The system instantly looks them up and shows their name,
   company, and what type of guest they are (Brand, Mill, Retailer, Press,
   etc.) — then marks them as "checked in" with the time.

2. **Company Verification Box** — Type in a company name (e.g. "Levi's").
   The system searches the internet live and checks if that company is
   actually connected to denim, jeans, or textiles. If it's not related
   (like a random bank or unrelated business), it gets rejected — no entry.

That's it. No paperwork, no manual lookup — just type and go.


This is a simple web tool with two main features:

Visitor Check-In — Staff type in a Visitor ID or phone number, and it instantly pulls up that person's name, company, and category, then marks them as checked in with a timestamp.
Company Verification — Type in any company name, and it searches the web live to check if that company is actually connected to the denim/textile industry. If not, entry is rejected.

What's in the database

One table called visitors, with these columns for each person:

Visitor ID
Name
Phone number
Company name
Category (Mill, Retailer, Brand, etc.)
Badge type (Visitor/Exhibitor/Speaker/Press)
Checked-in status (yes/no)
Check-in time
