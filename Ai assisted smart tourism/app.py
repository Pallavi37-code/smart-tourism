import streamlit as st
from database import init_db, save_trip, get_trips, delete_trip
from tourism_data import DESTINATIONS
from ai_engine import generate_itinerary, travel_assistant
from datetime import date

st.set_page_config(page_title="Smart Tourism & Travel Manager", page_icon="🌍", layout="wide")
init_db()

st.markdown("""
<style>
.main {background: #f7fafc;}
.hero {padding: 1.5rem 1.8rem; border-radius: 18px; background: linear-gradient(115deg,#0f766e,#2563eb); color:white;}
.hero h1 {color:white; margin:0;}
.hero p {color:#e0f2fe; margin-bottom:0;}
.metric-card {padding:14px;border-radius:14px;background:white;border:1px solid #e5e7eb;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🌍 Smart Travel")
    page = st.radio("Navigation", ["Home", "Explore Destinations", "AI Trip Planner", "Travel Assistant", "My Saved Trips", "About Project"])
    st.caption("AI-based Smart Tourism & Travel Management System")

if page == "Home":
    st.markdown('<div class="hero"><h1>Explore Smarter. Travel Better.</h1><p>Your personal tourism planner for discovering places, building itineraries and managing travel budgets.</p></div>', unsafe_allow_html=True)
    st.write("")
    c1,c2,c3 = st.columns(3)
    c1.metric("Destinations", len(DESTINATIONS))
    c2.metric("Core modules", 5)
    c3.metric("Trip storage", "SQLite")
    st.subheader("What you can do")
    cols = st.columns(3)
    cards = [
        ("🧭 Discover","Explore destinations by state, category, and estimated cost."),
        ("✨ Plan with AI","Generate a day-wise itinerary based on interests and budget."),
        ("💬 Ask the assistant","Get travel suggestions, packing tips and planning guidance."),
        ("💰 Estimate budget","See a practical approximate cost breakdown."),
        ("💾 Save trips","Store and revisit your plans using the local database."),
        ("🛡️ Travel smart","Review safety, best-season and responsible-tourism tips.")
    ]
    for col, (title, desc) in zip(cols*2, cards):
        with col:
            st.markdown(f"**{title}**")
            st.write(desc)
    st.info("This academic prototype uses a built-in destination knowledge base and AI-style recommendation engine. Add an API key in Settings/secrets to connect a live generative AI provider.")

elif page == "Explore Destinations":
    st.title("🧭 Explore Destinations")
    states = ["All"] + sorted(set(d["state"] for d in DESTINATIONS))
    categories = ["All"] + sorted(set(d["category"] for d in DESTINATIONS))
    a,b,c = st.columns(3)
    state = a.selectbox("State", states)
    category = b.selectbox("Travel type", categories)
    max_cost = c.slider("Maximum estimated daily budget (₹)", 500, 10000, 5000, 500)
    query = st.text_input("Search by destination or attraction")
    filtered = [d for d in DESTINATIONS if (state=="All" or d["state"]==state) and (category=="All" or d["category"]==category) and d["daily_cost"]<=max_cost and (query.lower() in (d["name"]+" "+d["state"]+" "+d["highlights"]).lower())]
    st.caption(f"{len(filtered)} destination(s) found")
    if not filtered:
        st.warning("No destinations match these filters. Try increasing your budget or changing the filters.")
    for d in filtered:
        with st.container(border=True):
            left,right = st.columns([3,1])
            with left:
                st.subheader(f'{d["emoji"]} {d["name"]}, {d["state"]}')
                st.write(d["description"])
                st.write("**Highlights:** " + d["highlights"])
                st.caption(f'Best season: {d["season"]} · Category: {d["category"]}')
            with right:
                st.metric("Approx. / day", f'₹{d["daily_cost"]:,}')
                st.metric("Suggested stay", f'{d["suggested_days"]} days')

elif page == "AI Trip Planner":
    st.title("✨ AI Trip Planner")
    st.write("Generate a personalized itinerary from your destination, travel dates, interests and budget.")
    names = [d["name"] for d in DESTINATIONS]
    with st.form("planner"):
        destination = st.selectbox("Destination", names)
        col1,col2,col3 = st.columns(3)
        start = col1.date_input("Start date", value=date.today())
        days = col2.number_input("Number of days", 1, 14, 3)
        travelers = col3.number_input("Number of travelers", 1, 20, 2)
        interests = st.multiselect("Interests", ["Nature","History","Culture","Adventure","Food","Spirituality","Photography","Shopping"], default=["Nature","Culture"])
        budget = st.number_input("Total budget (₹)", min_value=1000, value=15000, step=500)
        submitted = st.form_submit_button("Generate my trip", type="primary")
    if submitted:
        plan = generate_itinerary(destination, int(days), int(travelers), int(budget), interests)
        st.session_state["latest_plan"] = plan
        st.session_state["latest_meta"] = {"destination":destination,"start":str(start),"days":int(days),"travelers":int(travelers),"budget":int(budget),"interests":interests}
    if "latest_plan" in st.session_state:
        meta = st.session_state["latest_meta"]
        st.divider()
        st.subheader(f'Your {meta["days"]}-day plan for {meta["destination"]}')
        st.write(st.session_state["latest_plan"]["summary"])
        for day in st.session_state["latest_plan"]["days"]:
            with st.expander(day["title"], expanded=True):
                for item in day["activities"]:
                    st.markdown(f'- **{item["time"]}:** {item["activity"]}')
        st.subheader("Estimated budget")
        breakdown = st.session_state["latest_plan"]["budget"]
        b1,b2,b3,b4 = st.columns(4)
        b1.metric("Transport", f'₹{breakdown["transport"]:,}')
        b2.metric("Stay", f'₹{breakdown["stay"]:,}')
        b3.metric("Food & activities", f'₹{breakdown["food_activities"]:,}')
        b4.metric("Total", f'₹{breakdown["total"]:,}')
        if breakdown["total"] > meta["budget"]:
            st.warning("The estimate is above your entered budget. Reduce travel days or choose lower-cost options.")
        else:
            st.success("The estimate is within your entered budget.")
        if st.button("💾 Save this trip"):
            save_trip(meta, st.session_state["latest_plan"])
            st.success("Trip saved successfully!")

elif page == "Travel Assistant":
    st.title("💬 Smart Travel Assistant")
    st.write("Ask about destinations, itineraries, packing, budget planning or responsible travel.")
    if "chat" not in st.session_state: st.session_state.chat = []
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    prompt = st.chat_input("Example: Suggest a 2-day nature trip under ₹8,000")
    if prompt:
        st.session_state.chat.append({"role":"user","content":prompt})
        answer = travel_assistant(prompt)
        st.session_state.chat.append({"role":"assistant","content":answer})
        st.rerun()

elif page == "My Saved Trips":
    st.title("💾 My Saved Trips")
    trips = get_trips()
    if not trips:
        st.info("No saved trips yet. Generate a plan in AI Trip Planner and save it.")
    for trip in trips:
        with st.expander(f'{trip["destination"]} · {trip["created_at"]}'):
            st.write(f'Dates: {trip["start_date"]} | Days: {trip["days"]} | Travelers: {trip["travelers"]}')
            st.write(f'Budget: ₹{trip["budget"]:,}')
            st.write(trip["summary"])
            if st.button("Delete trip", key=f'del_{trip["id"]}'):
                delete_trip(trip["id"])
                st.rerun()

else:
    st.title("📘 About the Project")
    st.markdown("""
**Project title:** AI-Based Smart Tourism and Travel Management System

**Domain:** Artificial Intelligence, Tourism, Travel Management and Web Application Development.

**Problem addressed:** Travelers often need to visit multiple websites and manually compare destinations, interests, budgets and schedules. This can make trip planning time-consuming.

**Proposed solution:** A single web application that provides destination discovery, personalized itinerary generation, approximate budget estimation, a travel assistant and saved-trip management.

**Novelty:** The recommendation workflow combines user interests, trip duration and budget to generate a structured day-wise plan. The prototype is designed to be extendable with live maps, weather, hotel and transport APIs.

**Important note:** Destination details and prices are illustrative estimates for an academic prototype. Verify current transport, entry fees, weather, local rules and safety information before real travel.
""")
    st.subheader("Technology stack")
    st.write("Python · Streamlit · SQLite · Pandas-free lightweight logic · Rule-based AI recommendation engine")
    st.subheader("Suggested future enhancements")
    st.write("Live LLM integration, maps and route optimization, real-time weather, hotel/flight APIs, multilingual support, user login and admin analytics.")
