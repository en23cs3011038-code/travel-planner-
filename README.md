# Personalized Travel Itinerary Planner

College project: user ki preferences (destination, din, budget, interests, travel style) ke hisaab se din-ba-din travel itinerary generate karne wali web app.

**Tech stack:** Python (Flask), SQLite (SQL), HTML, CSS (Jinja2 templates)

## Run kaise karein

```bash
pip install -r requirements.txt
python init_db.py      # database + sample data (pehli baar)
python app.py          # http://127.0.0.1:5000 par kholein
```

## Project structure

```
travel-planner/
├── app.py             # Flask routes + itinerary logic + budget calculation
├── init_db.py         # SQL schema + sample data (Goa, Jaipur, Manali)
├── requirements.txt
├── templates/         # base, index (form), itinerary, history
└── static/style.css
```

## Database (SQL)

- `destinations` (id, name, state, description)
- `places` (id, destination_id, name, category, cost, best_time, description)
- `trips` (id, destination_id, days, travelers, budget, style, interests, total_cost, created_at)

`places.destination_id` aur `trips.destination_id`, dono `destinations.id` ke foreign key hain.

## Itinerary algorithm

1. Chosen destination ke saare places database se lete hain.
2. User ke interests wale places ko priority dete hain.
3. Har din ke 3 slots (morning / afternoon / evening) bharte hain, pehle sahi `best_time` wala place, phir koi bhi interest wala, phir baaki.
4. Ek place dobara repeat nahi hota.
5. Cost = (activity cost + daily stay/food cost) x travelers, phir budget se compare.

## Future scope

- Zyada cities aur places (admin panel se add karna)
- Login ke saath saved/editable itineraries
- Google Maps integration
- Weather API
- AI (LLM) se personalised descriptions
- PDF download
