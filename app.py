import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for

import init_db

DB = "travel.db"
SLOTS = ["morning", "afternoon", "evening"]
INTERESTS = ["Adventure", "Food", "History", "Nature", "Relaxation", "Shopping"]

# Rooms + khana + local transport ka rough kharcha, per person per day (INR)
DAILY_COST = {"budget": 1500, "standard": 3000, "luxury": 7000}

app = Flask(__name__)

if not os.path.exists(DB):
    init_db.init()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def generate_itinerary(dest_id, days, interests, style, travelers, budget):
    """Interests ke hisaab se har din ke 3 slots (subah/dopahar/shaam) bharta hai."""
    db = get_db()
    rows = db.execute("SELECT * FROM places WHERE destination_id = ?", (dest_id,)).fetchall()
    places = [dict(r) for r in rows]

    # Pehle user ke interests wale places, phir baaki (fallback)
    preferred = [p for p in places if p["category"] in interests]
    others = [p for p in places if p["category"] not in interests]

    used = set()
    plan = []

    def pick(slot):
        # 1) interest + sahi time, 2) interest + koi bhi time,
        # 3) koi bhi place sahi time pe, 4) koi bhi bacha hua place
        for pool, need_slot in (
            (preferred, True), (preferred, False), (others, True), (others, False)
        ):
            for p in pool:
                if p["id"] in used:
                    continue
                if need_slot and p["best_time"] != slot:
                    continue
                used.add(p["id"])
                return p
        return None

    for d in range(1, days + 1):
        day = {"day": d, "slots": []}
        for slot in SLOTS:
            day["slots"].append({"slot": slot, "place": pick(slot)})
        plan.append(day)

    activity_cost = sum(
        s["place"]["cost"] for day in plan for s in day["slots"] if s["place"]
    ) * travelers
    stay_food_cost = DAILY_COST[style] * days * travelers
    total = activity_cost + stay_food_cost

    return {
        "plan": plan,
        "activity_cost": activity_cost,
        "stay_food_cost": stay_food_cost,
        "total": total,
        "within_budget": total <= budget,
        "difference": abs(budget - total),
    }


@app.route("/")
def index():
    dests = get_db().execute("SELECT * FROM destinations ORDER BY name").fetchall()
    return render_template("index.html", destinations=dests, interests=INTERESTS)


@app.route("/plan", methods=["POST"])
def plan():
    db = get_db()
    try:
        dest_id = int(request.form["destination"])
        days = max(1, min(int(request.form["days"]), 10))
        travelers = max(1, min(int(request.form["travelers"]), 20))
        budget = max(1000, int(request.form["budget"]))
    except (KeyError, ValueError):
        return redirect(url_for("index"))

    style = request.form.get("style", "standard")
    if style not in DAILY_COST:
        style = "standard"
    interests = [i for i in request.form.getlist("interests") if i in INTERESTS]
    if not interests:
        interests = INTERESTS  # kuch select na kare to sab maan lo

    dest = db.execute("SELECT * FROM destinations WHERE id = ?", (dest_id,)).fetchone()
    if dest is None:
        return redirect(url_for("index"))

    result = generate_itinerary(dest_id, days, interests, style, travelers, budget)

    db.execute(
        "INSERT INTO trips (destination_id, days, travelers, budget, style, interests, total_cost) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (dest_id, days, travelers, budget, style, ", ".join(interests), result["total"]),
    )
    db.commit()

    return render_template(
        "itinerary.html",
        dest=dest, days=days, travelers=travelers, budget=budget,
        style=style, interests=interests, result=result,
    )


@app.route("/history")
def history():
    trips = get_db().execute(
        "SELECT t.*, d.name AS dest_name FROM trips t "
        "JOIN destinations d ON d.id = t.destination_id "
        "ORDER BY t.id DESC LIMIT 20"
    ).fetchall()
    return render_template("history.html", trips=trips)


if __name__ == "__main__":
    app.run(debug=True)
