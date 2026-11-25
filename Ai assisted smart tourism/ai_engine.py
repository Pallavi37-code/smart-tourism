from tourism_data import DESTINATIONS


def find_destination(name):
    return next((d for d in DESTINATIONS if d["name"].lower() == name.lower()), DESTINATIONS[0])


def generate_itinerary(destination, days, travelers, total_budget, interests):
    d = find_destination(destination)
    highlights = [x.strip() for x in d["highlights"].split(",")]
    interest_words = [x.lower() for x in interests]
    # Reorder a small set of attractions using simple interest matching.
    if any(x in interest_words for x in ["nature", "adventure", "photography"]):
        highlights = highlights[::-1]

    activities = []
    for day in range(days):
        place1 = highlights[(day * 2) % len(highlights)]
        place2 = highlights[(day * 2 + 1) % len(highlights)]
        place3 = highlights[(day * 2 + 2) % len(highlights)]
        activities.append({
            "title": f"Day {day + 1} — Explore {d['name']}",
            "activities": [
                {"time": "Morning", "activity": f"Visit {place1}; start early and allow time for local transport."},
                {"time": "Afternoon", "activity": f"Explore {place2}; enjoy a local lunch and learn about the area."},
                {"time": "Evening", "activity": f"Visit {place3} or enjoy a relaxed local experience."}
            ]
        })

    per_person_day = d["daily_cost"]
    estimate = per_person_day * days * travelers
    transport = round(estimate * 0.22)
    stay = round(estimate * 0.35)
    food_activities = max(0, estimate - transport - stay)
    budget_note = "This plan is within your target budget." if total_budget and estimate <= total_budget else "This plan exceeds your target budget; consider fewer paid activities or shorter stays."
    return {
        "summary": (
            f"A {days}-day plan for {travelers} traveler(s) in {d['name']}, focused on "
            f"{', '.join(interests) if interests else 'general sightseeing'}. "
            f"Approximate estimate: ₹{estimate:,}. {budget_note}"
        ),
        "days": activities,
        "budget": {"transport": transport, "stay": stay, "food_activities": food_activities, "total": estimate}
    }

def travel_assistant(question):
    q = question.lower()
    if any(w in q for w in ["budget","cost","cheap","₹","rupee"]):
        return ("For a useful budget, estimate transport, accommodation, food, entry tickets and a 10–15% contingency. "
                "Choose a destination and travel dates in AI Trip Planner for an approximate breakdown. Estimates in this demo are illustrative, not live prices.")
    if any(w in q for w in ["pack","packing","carry"]):
        return ("Packing checklist: valid ID, booking details, weather-appropriate clothing, comfortable footwear, medicines you normally use, "
                "phone charger/power bank, reusable water bottle and a small first-aid kit. Check baggage and local rules before departure.")
    if any(w in q for w in ["safe","safety","emergency"]):
        return ("Travel safely: share your itinerary with someone you trust, use registered transport, keep emergency contacts accessible, "
                "check local advisories and weather, protect valuables, and respect local customs and protected areas.")
    matches = [d for d in DESTINATIONS if d["name"].lower() in q or d["state"].lower() in q]
    if matches:
        d = matches[0]
        return f'{d["name"]}, {d["state"]}: {d["description"]} Highlights include {d["highlights"]}. A common suggested visit is {d["suggested_days"]} days. Best season listed in this demo: {d["season"]}.'
    return ("I can help with destination ideas, itinerary planning, budgets, packing and travel safety. "
            "Try asking: 'Suggest a nature trip', 'How should I plan my budget?' or 'What should I pack?'")
