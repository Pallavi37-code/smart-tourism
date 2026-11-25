# AI-Based Smart Tourism and Travel Management System

A runnable academic prototype built with Python, Streamlit and SQLite.

## Features
- Destination discovery with state, category, search and daily-budget filters
- AI-style day-wise itinerary generation from destination, duration, interests and budget
- Approximate budget split for transport, stay, food and activities
- Travel assistant for destination information, budgeting, packing and safety
- Save and delete trips using SQLite
- Project overview page for demonstration

## Run on Windows (VS Code)
1. Extract the ZIP file.
2. Open the extracted folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the application:
   ```bash
   streamlit run app.py
   ```
7. Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.

## Database
The app automatically creates `smart_tourism.db` in the project folder when it first runs. Saved trips are stored there. Use **My Saved Trips** to delete an individual trip. To reset all saved trips, stop the app and delete `smart_tourism.db`; it will be recreated on the next run.

## Important academic note
The current version uses a transparent, rule-based recommendation engine (an AI-style decision module), not a trained machine-learning model or live LLM. Destination costs are illustrative estimates and must not be presented as real-time prices. Live maps, weather, hotel/flight booking and an LLM API can be integrated as future enhancements.

## Suggested demo flow
1. Home dashboard
2. Explore Destinations: filter Telangana and search Warangal
3. AI Trip Planner: choose a destination, 2–3 days, interests and budget
4. Show itinerary and budget estimate
5. Save trip, open My Saved Trips, and delete the saved record
6. Ask the Travel Assistant about budget or safety
