"""Database banata hai (SQLite) aur sample data bharta hai.
Run: python init_db.py
"""
import sqlite3

DB = "travel.db"

SCHEMA = """
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS destinations;

CREATE TABLE destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    state TEXT NOT NULL,
    description TEXT
);

CREATE TABLE places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,      -- Adventure / Food / History / Nature / Relaxation / Shopping
    cost INTEGER NOT NULL,       -- entry / activity cost per person (INR)
    best_time TEXT NOT NULL,     -- morning / afternoon / evening
    description TEXT,
    FOREIGN KEY (destination_id) REFERENCES destinations(id)
);

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    days INTEGER NOT NULL,
    travelers INTEGER NOT NULL,
    budget INTEGER NOT NULL,
    style TEXT NOT NULL,
    interests TEXT NOT NULL,
    total_cost INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destination_id) REFERENCES destinations(id)
);
"""

DESTINATIONS = [
    ("Goa", "Goa", "Beaches, nightlife, Portuguese heritage aur seafood."),
    ("Jaipur", "Rajasthan", "Pink City: forts, palaces aur shaandar bazaars."),
    ("Manali", "Himachal Pradesh", "Pahadi vadiyan, adventure sports aur cafes."),
]

# (destination_name, place, category, cost, best_time, description)
PLACES = [
    # ---- Goa ----
    ("Goa", "Fort Aguada", "History", 0, "morning", "17vi sadi ka Portuguese fort, samundar ka nazara."),
    ("Goa", "Basilica of Bom Jesus", "History", 0, "morning", "UNESCO World Heritage church, Old Goa."),
    ("Goa", "Chapora Fort Sunset", "History", 0, "evening", "Dil Chahta Hai wala fort, sunset ke liye best."),
    ("Goa", "Dudhsagar Waterfall", "Nature", 500, "morning", "Jeep safari ke saath badh jharna."),
    ("Goa", "Spice Plantation Tour", "Nature", 600, "morning", "Masalon ke bagicho ka tour, lunch included."),
    ("Goa", "Water Sports at Calangute", "Adventure", 1500, "afternoon", "Parasailing, jet ski, banana boat."),
    ("Goa", "Scuba at Grande Island", "Adventure", 2500, "morning", "Beginners ke liye bhi scuba diving."),
    ("Goa", "Goan Fish Thali", "Food", 500, "afternoon", "Traditional Goan seafood thali."),
    ("Goa", "Dinner at Fisherman's Wharf", "Food", 900, "evening", "River-side seafood dinner."),
    ("Goa", "Baga Beach", "Relaxation", 0, "evening", "Beach shacks, music aur sunset."),
    ("Goa", "Palolem Beach", "Relaxation", 0, "afternoon", "Shaant, kam bheed wala beach (South Goa)."),
    ("Goa", "Anjuna Flea Market", "Shopping", 0, "afternoon", "Handicrafts, kapde aur souvenirs."),
    # ---- Jaipur ----
    ("Jaipur", "Amber Fort", "History", 500, "morning", "Hill-top fort, Sheesh Mahal ke saath."),
    ("Jaipur", "Hawa Mahal", "History", 200, "morning", "953 jharokhon wala iconic mahal."),
    ("Jaipur", "City Palace", "History", 700, "afternoon", "Royal family ka palace aur museum."),
    ("Jaipur", "Jantar Mantar", "History", 200, "afternoon", "UNESCO site, purani astronomical yantra."),
    ("Jaipur", "Albert Hall Museum", "History", 300, "afternoon", "Rajasthani art aur artifacts."),
    ("Jaipur", "Rawat Kachori & Lassi", "Food", 300, "morning", "Jaipur ka famous nashta."),
    ("Jaipur", "Dinner at Chokhi Dhani", "Food", 900, "evening", "Rajasthani village theme, folk dance ke saath."),
    ("Jaipur", "Nahargarh Fort Sunset", "Nature", 200, "evening", "Poore shehar ka panoramic view."),
    ("Jaipur", "Jaigarh Fort Jeep Safari", "Adventure", 800, "afternoon", "Jeep ride aur duniya ki bahut badi toap."),
    ("Jaipur", "Jal Mahal Viewpoint", "Relaxation", 0, "evening", "Jheel ke beech bana mahal."),
    ("Jaipur", "Johari Bazaar", "Shopping", 0, "evening", "Jewellery aur gems ka bazaar."),
    ("Jaipur", "Bapu Bazaar", "Shopping", 0, "afternoon", "Juti, kapde aur handicrafts."),
    # ---- Manali ----
    ("Manali", "Hadimba Devi Temple", "History", 0, "morning", "Deodar jungle ke beech lakdi ka mandir."),
    ("Manali", "Tibetan Monastery", "History", 0, "afternoon", "Shaant monastery aur local handicrafts."),
    ("Manali", "Manu Temple", "History", 0, "morning", "Old Manali ka prachin mandir."),
    ("Manali", "Rohtang Pass", "Nature", 1500, "morning", "Barf ke pahad (permit zaruri)."),
    ("Manali", "Jogini Waterfall Trek", "Nature", 0, "afternoon", "Aasan trek, sundar jharna."),
    ("Manali", "Paragliding at Solang Valley", "Adventure", 3000, "morning", "Himalaya ke upar udaan."),
    ("Manali", "River Rafting in Kullu", "Adventure", 1200, "afternoon", "Beas nadi par rafting."),
    ("Manali", "Old Manali Cafe Hopping", "Food", 600, "afternoon", "Israeli food aur live music cafes."),
    ("Manali", "Siddu & Trout Dinner", "Food", 700, "evening", "Himachali siddu aur fresh trout fish."),
    ("Manali", "Vashisht Hot Springs", "Relaxation", 0, "afternoon", "Garam paani ke kund."),
    ("Manali", "Beas Riverside Walk", "Relaxation", 0, "evening", "Shaam ki sukoon bhari sair."),
    ("Manali", "Mall Road", "Shopping", 0, "evening", "Woollens, shawls aur street food."),
]


def init():
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    ids = {}
    for name, state, desc in DESTINATIONS:
        cur = conn.execute(
            "INSERT INTO destinations (name, state, description) VALUES (?, ?, ?)",
            (name, state, desc),
        )
        ids[name] = cur.lastrowid
    for dest, name, cat, cost, best, desc in PLACES:
        conn.execute(
            "INSERT INTO places (destination_id, name, category, cost, best_time, description) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (ids[dest], name, cat, cost, best, desc),
        )
    conn.commit()
    conn.close()
    print("Database ready:", DB)


if __name__ == "__main__":
    init()
