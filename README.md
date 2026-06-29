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

---

## What you need before starting

- A computer with internet access
- Two free accounts (we'll create these together, no credit card needed):
  - A [GitHub](https://github.com) account — this is just a place to store
    the project's files online
  - A [Render](https://render.com) account — this is what actually runs
    the website live, 24/7

You don't need to understand code to follow the steps below — just copy,
paste, and click where instructed.

---

## How to run it on your own computer first (recommended before going live)

This lets you test everything before sharing the link with anyone.

1. **Install Python** (if you don't already have it):
   Go to [python.org/downloads](https://www.python.org/downloads) and
   install the latest version. Just click through the installer normally.

2. **Open a terminal** (on Windows: search "Command Prompt"; on Mac:
   search "Terminal").

3. **Go into the project folder**:
   ```
   cd checkin_system
   ```

4. **Install the required pieces** (one-time setup):
   ```
   pip install flask requests beautifulsoup4 gunicorn
   ```

5. **Start the website**:
   ```
   python3 app.py
   ```

6. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

   You should see the check-in page. Try typing `DJ001` in the first box,
   or `Levi's` in the second box, to see it work.

7. To stop it, go back to the terminal and press `Ctrl + C`.

---

## How to put this live on the internet (so anyone can use it from a link)

We're using a free service called **Render** to host it.

### Step 1 — Put the project on GitHub
This is just a way of "uploading" your project so Render can find it.

1. Go to [github.com](https://github.com) and sign up (free).
2. Click the **+** icon (top right) → **New repository**.
3. Name it something like `checkin-system`, leave everything else default,
   click **Create repository**.
4. Follow GitHub's instructions on that page to upload your project folder
   (it will show you simple copy-paste commands).

### Step 2 — Connect Render to GitHub
1. Go to [render.com](https://render.com) and sign up using your GitHub
   account (this is the easiest option — one click).
2. Click **New +** (top right) → **Web Service**.
3. Pick the `checkin-system` project you just uploaded.

### Step 3 — Fill in a few settings
Render will ask a few questions. Use these exact answers:

| Setting | What to type |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Instance Type | Free |

Then click **Create Web Service**.

### Step 4 — Wait and get your link
Render will take 1-2 minutes to set everything up. When it's done, you'll
see a link at the top that looks like:

```
https://checkin-system-xxxx.onrender.com
```

That's your live website! Share this link with anyone — they can check
people in or verify companies from any phone or computer, no installation
needed.

---

## A few honest things to know

- **The free version "sleeps" when nobody uses it.** If nobody visits the
  page for about 15 minutes, it goes to sleep to save resources. The very
  next person to open the link might wait 30-50 seconds for it to "wake
  up" — totally normal, just a one-time delay.

- **The visitor list resets if we update the website.** Right now, the
  list of registered visitors is stored in a simple file that lives on the
  free server. If we ever push an update to the website, this list starts
  fresh again. This is fine for testing and demos. Before using this for a
  real, ongoing show, we should upgrade to a proper database that doesn't
  reset — just let me know when you're ready for that step and I'll set
  it up.

- **Company verification needs internet on the server.** Since it
  searches the web live for each company, if the internet connection on
  Render's side has any hiccup, it will say "lookup failed" rather than
  guessing — this is intentional, so it never wrongly approves or rejects
  someone by mistake.

---

## If something doesn't work

- **Page won't load locally** → Make sure you ran `python3 app.py` and
  the terminal shows it's running, then open `http://localhost:5000`
  (not the file itself).
- **"Module not found" error** → Run the `pip install` command from Step 4
  above again.
- **Render deployment fails** → Double check the Build Command and Start
  Command match exactly what's in the table above.

If you get stuck on anything, just describe what you see and I'll help
figure it out.
