import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv(override=True)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Agent — Plan Any Trip, Anywhere",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stSidebarNav"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
header[data-testid="stHeader"] { display: none; }
#MainMenu { display: none; }
footer { display: none; }

/* Animated background */
.stApp {
    background: linear-gradient(145deg, #060d1a 0%, #0a1628 40%, #0c2035 100%);
    color: #f0f4f8;
    min-height: 100vh;
}

/* Floating orbs animation */
.stApp::before {
    content: '';
    position: fixed;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(26,115,232,0.08) 0%, transparent 70%);
    top: -200px; left: -200px;
    border-radius: 50%;
    animation: float1 12s ease-in-out infinite;
    pointer-events: none; z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(108,63,197,0.07) 0%, transparent 70%);
    bottom: -150px; right: -150px;
    border-radius: 50%;
    animation: float2 15s ease-in-out infinite;
    pointer-events: none; z-index: 0;
}
@keyframes float1 {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(60px,40px) scale(1.1); }
}
@keyframes float2 {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(-50px,-30px) scale(1.08); }
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
    position: relative; z-index: 1;
}

/* ── PLANE ANIMATION ── */
@keyframes flyIn {
    0%   { transform: translateX(-120px) translateY(6px) rotate(-5deg); opacity: 0; }
    60%  { transform: translateX(8px) translateY(-3px) rotate(2deg); opacity: 1; }
    80%  { transform: translateX(-4px) translateY(0px) rotate(0deg); }
    100% { transform: translateX(0px) translateY(0px) rotate(0deg); opacity: 1; }
}
@keyframes titleFadeIn {
    from { opacity: 0; transform: translateX(30px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* ── HERO HEADER ── */
@keyframes slideDown {
    from { opacity:0; transform: translateY(-20px); }
    to   { opacity:1; transform: translateY(0); }
}
.hero-header {
    background: linear-gradient(135deg, #ffffff 0%, #f0f6ff 50%, #f5f0ff 100%);
    border-radius: 20px;
    padding: 20px 40px;
    margin-bottom: 16px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.15), inset 0 1px 0 rgba(255,255,255,0.8);
    display: flex;
    align-items: center;
    justify-content: space-between;
    animation: slideDown 0.6s ease-out;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 900;
    line-height: 1.1;
    margin: 0;
    letter-spacing: -1px;
}
.plane-icon {
    display: inline-block;
    font-style: normal;
    animation: flyIn 1s cubic-bezier(0.22,1,0.36,1) both;
}
.title-text {
    display: inline-block;
    background: linear-gradient(90deg, #1a73e8 0%, #6c3fc5 50%, #e8416a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleFadeIn 0.7s ease-out 0.5s both;
}
.hero-sub {
    font-size: 15px;
    color: #5a6e85;
    margin-top: 8px;
    font-weight: 500;
    letter-spacing: 0.2px;
}
.hero-badges { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
.badge {
    background: linear-gradient(135deg, #e8f4ff, #f0e8ff);
    border: 1px solid rgba(58,123,213,0.25);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #2a5298;
    font-weight: 600;
    animation: fadeIn 0.8s ease-out both;
}
@keyframes fadeIn {
    from { opacity:0; transform: scale(0.9); }
    to   { opacity:1; transform: scale(1); }
}
.hero-status { text-align: right; min-width: 210px; }
.status-row { font-size: 13px; color: #4a6080; margin: 5px 0; font-weight: 500; }

/* ── PROMPT PANEL ── */
@keyframes slideInRight {
    from { opacity:0; transform: translateX(20px); }
    to   { opacity:1; transform: translateX(0); }
}
.prompt-panel {
    background: #060e1a;
    border: 1px solid #1a3050;
    border-radius: 20px;
    padding: 20px 14px 16px;
    animation: slideInRight 0.5s ease-out;
}
.prompt-panel-title {
    font-size: 11px;
    font-weight: 700;
    color: #74b9ff;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 12px;
    padding: 0 4px;
}
.powered-by {
    font-size: 11px;
    color: #2a4a6a;
    text-align: center;
    margin-top: 14px;
    font-weight: 500;
}

/* ── ALL prompt buttons in the panel ── */
.prompt-panel div[data-testid="stButton"] button,
.prompt-panel ~ div div[data-testid="stButton"] button {
    background: #0d1e30 !important;
    border: 1px solid #1e3a55 !important;
    border-radius: 11px !important;
    color: #a8cce8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 11px 14px !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 46px !important;
    line-height: 1.45 !important;
    transition: all 0.2s ease !important;
    margin-bottom: 2px !important;
}
.prompt-panel div[data-testid="stButton"] button:hover,
.prompt-panel ~ div div[data-testid="stButton"] button:hover {
    background: #162d48 !important;
    border-color: #4a90d9 !important;
    color: #ffffff !important;
    transform: translateX(4px) !important;
    box-shadow: 0 4px 16px rgba(58,123,213,0.3) !important;
}
.prompt-panel div[data-testid="stButton"] button p,
.prompt-panel ~ div div[data-testid="stButton"] button p {
    color: inherit !important;
    font-size: inherit !important;
}

/* Nuclear override — all buttons app-wide */
button[kind="secondary"], button[data-testid="baseButton-secondary"] {
    background: #0d1e30 !important;
    border: 1px solid #1e3a55 !important;
    border-radius: 11px !important;
    color: #a8cce8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 11px 14px !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 46px !important;
    transition: all 0.2s ease !important;
}
button[kind="secondary"]:hover, button[data-testid="baseButton-secondary"]:hover {
    background: #162d48 !important;
    border-color: #4a90d9 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 16px rgba(58,123,213,0.3) !important;
}
button[kind="secondary"] p, button[data-testid="baseButton-secondary"] p {
    color: #a8cce8 !important;
}
button[kind="secondary"]:hover p, button[data-testid="baseButton-secondary"]:hover p {
    color: #ffffff !important;
}

/* ── CHAT ── */
@keyframes slideInLeft {
    from { opacity:0; transform: translateX(-15px); }
    to   { opacity:1; transform: translateX(0); }
}
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 8px;
    margin: 10px 0;
    animation: slideInLeft 0.3s ease-out;
    backdrop-filter: blur(8px);
}
[data-testid="stChatInput"] {
    padding: 14px 20px !important;
    background: rgba(6,13,26,0.95) !important;
    border-top: 1px solid rgba(58,123,213,0.2) !important;
    backdrop-filter: blur(10px);
}
[data-testid="stChatInput"] > div { background: transparent !important; }
[data-testid="stChatInput"] textarea {
    background: #0a1a28 !important;
    border: 2px solid #1e3a5f !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-size: 16px !important;
    min-height: 60px !important;
    padding: 18px 22px !important;
    caret-color: #74b9ff !important;
    -webkit-text-fill-color: #ffffff !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #3a6080 !important;
    -webkit-text-fill-color: #3a6080 !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #74b9ff !important;
    box-shadow: 0 0 0 3px rgba(116,185,255,0.12), 0 4px 20px rgba(0,0,0,0.3) !important;
    background: #0d1f2d !important;
}

/* ── MARKDOWN ── */
hr { border-color: rgba(255,255,255,0.08) !important; }
.stMarkdown p, .stMarkdown li { color: #cddcee; line-height: 1.8; font-size: 15px; }
.stMarkdown h2 {
    color: #74b9ff;
    border-bottom: 1px solid rgba(116,185,255,0.2);
    padding-bottom: 8px; margin-top: 28px;
    font-size: 1.25rem; font-weight: 700;
}
.stMarkdown h3 { color: #a29bfe; font-size: 1.05rem; font-weight: 600; }
.stMarkdown table { border-collapse: collapse; width: 100%; margin: 16px 0; border-radius: 10px; overflow: hidden; }
.stMarkdown th { background: rgba(26,115,232,0.2); color: #74b9ff; padding: 11px 16px; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
.stMarkdown td { padding: 10px 16px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #cddcee; font-size: 14px; }
.stMarkdown tr:hover td { background: rgba(58,123,213,0.06); }
.stMarkdown code { background: rgba(116,185,255,0.1); border-radius: 5px; padding: 2px 8px; color: #cddcee; font-size: 13px; }
.stMarkdown blockquote { border-left: 3px solid #74b9ff; padding-left: 16px; color: #8ab4d4; font-style: italic; }

/* Welcome screen */
.welcome-screen {
    text-align: center;
    padding: 60px 20px 40px;
    animation: fadeIn 0.7s ease-out;
}
.welcome-globe { font-size: 72px; margin-bottom: 20px; display: block; animation: pulse 2s ease-in-out infinite; }
@keyframes pulse {
    0%,100% { transform: scale(1); }
    50% { transform: scale(1.06); }
}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a fully autonomous personal travel agent covering every destination worldwide.

You are NOT a conversational chatbot. You are an action-oriented planning agent that independently creates complete, practical, real-world travel plans without asking follow-up questions.

You have access to real-time tools:
- get_weather: Fetch live weather forecasts for any city
- search_flights: Estimate flight options between cities (knowledge-based)
- search_hotels: Estimate hotel options in a city (knowledge-based)

ALWAYS use get_weather for every major destination. Use search_flights and search_hotels to provide structured estimates.

Operating mode:
- Fully autonomous — no follow-up questions ever
- Make reasonable assumptions, state them once, then proceed
- If a tool returns an error, fall back to your knowledge and note it

Geographic scope: Worldwide — every country and continent

Output format — always use ALL these sections with markdown:
## Assumptions
## Route & Itinerary (day-by-day)
## Transport Plan
## Stay Areas & Hotels
## Budget Estimate (use a markdown table)
## Weather Summary
## Visa & Entry Requirements (always include: visa type, cost, how to apply, duration)
## Practical Tips (safety, scams, cultural norms, what to pack)

Style: Structured, actionable, no fluff. Use markdown tables and bullet points.

IMPORTANT FORMATTING RULES:
- Never use backticks around numbers or prices
- Write prices as plain text: e.g. ₹5,000 or $200-300 (never use code formatting for prices)
- In budget tables use plain numbers only, no backticks
- Do not use code blocks for anything except actual code"""

# ── Tool definitions (for Groq function calling) ──────────────────────────────
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get live weather forecast for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name e.g. 'Mumbai', 'Bangkok', 'Jaipur'"},
                    "days": {"type": "integer", "description": "Forecast days 1-7, default 5"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": "Provide flight route information and typical fare estimates between two cities",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "Origin city or airport code e.g. 'Delhi', 'DEL'"},
                    "destination": {"type": "string", "description": "Destination city or airport code"},
                    "travel_class": {"type": "string", "enum": ["economy", "business"], "description": "Travel class"},
                },
                "required": ["origin", "destination"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": "Provide hotel area recommendations and typical price ranges for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name e.g. 'Jaipur', 'Bangkok'"},
                    "budget_level": {"type": "string", "enum": ["budget", "mid-range", "luxury"], "description": "Budget level"},
                    "nights": {"type": "integer", "description": "Number of nights"},
                },
                "required": ["city"],
            },
        },
    },
]

TOOL_ICONS = {
    "get_weather": "🌤️",
    "search_flights": "✈️",
    "search_hotels": "🏨",
    "remember_preference": "🧠",
    "recall_preferences": "🧠",
}

# ── Tool implementations ───────────────────────────────────────────────────────
def get_weather(city: str, days: int = 5) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return {"error": "No API key", "fallback": "Using knowledge-based weather assessment"}
    try:
        geo = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}",
            timeout=8, verify=False
        ).json()
        if not geo:
            return {"error": f"City not found: {city}"}
        lat, lon = geo[0]["lat"], geo[0]["lon"]
        data = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?lat={lat}&lon={lon}&appid={api_key}&units=metric&cnt={min(days,7)*8}",
            timeout=8, verify=False
        ).json()
        daily = {}
        for item in data.get("list", []):
            date = item["dt_txt"].split(" ")[0]
            if date not in daily:
                daily[date] = {
                    "date": date,
                    "temp_min_c": round(item["main"]["temp_min"]),
                    "temp_max_c": round(item["main"]["temp_max"]),
                    "condition": item["weather"][0]["description"],
                    "humidity_pct": item["main"]["humidity"],
                    "wind_kmh": round(item["wind"]["speed"] * 3.6),
                }
        return {"city": city, "forecast": list(daily.values())[:days]}
    except Exception as e:
        return {"error": str(e)}


def search_flights(origin: str, destination: str, travel_class: str = "economy") -> dict:
    return {
        "origin": origin,
        "destination": destination,
        "travel_class": travel_class,
        "note": "Provide realistic fare estimates based on your knowledge of this route. Include typical airlines, duration, and INR price range.",
    }


def search_hotels(city: str, budget_level: str = "mid-range", nights: int = 2) -> dict:
    return {
        "city": city,
        "budget_level": budget_level,
        "nights": nights,
        "note": "Provide realistic hotel area recommendations and INR price ranges per night based on your knowledge.",
    }


# ── Memory tools — Neon PostgreSQL ────────────────────────────────────────────
import psycopg2
from psycopg2.extras import RealDictCursor

def _get_db():
    return psycopg2.connect(
        os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_k1TlFyVsHz5o@ep-raspy-credit-anqhzo5x.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require")
    )

def _init_db():
    """Create preferences table if it doesn't exist."""
    try:
        conn = _get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        pass

# Init table on startup
_init_db()

def remember_preference(key: str, value: str) -> dict:
    """Save a user preference or fact for future trips.
    Args:
        key: Category e.g. 'travel_style', 'budget_level', 'home_city', 'dietary', 'interests'
        value: The value e.g. 'mid-range', 'Delhi', 'vegetarian', 'adventure travel'
    """
    try:
        conn = _get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_preferences (key, value, updated_at)
            VALUES (%s, %s, NOW())
            ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()
        """, (key, value))
        conn.commit()
        cur.close()
        conn.close()
        return {"saved": True, "key": key, "value": value}
    except Exception as e:
        return {"saved": False, "error": str(e)}

def recall_preferences() -> dict:
    """Recall all saved user preferences to personalize the travel plan."""
    try:
        conn = _get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT key, value FROM user_preferences ORDER BY updated_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if rows:
            prefs = {r["key"]: r["value"] for r in rows}
            return {"preferences": prefs}
        return {"preferences": {}, "note": "No preferences saved yet"}
    except Exception as e:
        return {"preferences": {}, "error": str(e)}

TOOL_MAP = {
    "get_weather": get_weather,
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "remember_preference": remember_preference,
    "recall_preferences": recall_preferences,
}

# ── Updated tool schemas ───────────────────────────────────────────────────────
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get live 5-day weather forecast for a city. Call this for EVERY city in the itinerary.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name e.g. 'Mumbai', 'Bangkok', 'Jaipur'"},
                    "days": {"type": "integer", "description": "Forecast days 1-7, default 5"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": "Get flight route information and typical fare estimates between two cities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "Origin city or airport code"},
                    "destination": {"type": "string", "description": "Destination city or airport code"},
                    "travel_class": {"type": "string", "enum": ["economy", "business"], "description": "Travel class"},
                },
                "required": ["origin", "destination"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": "Get hotel area recommendations and typical price ranges for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name e.g. 'Jaipur', 'Bangkok'"},
                    "budget_level": {"type": "string", "enum": ["budget", "mid-range", "luxury"]},
                    "nights": {"type": "integer", "description": "Number of nights"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remember_preference",
            "description": "Save a user preference for future trips. Call this when user mentions travel style, budget, home city, dietary needs, or interests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Preference category: travel_style, budget_level, home_city, dietary, interests, group_size"},
                    "value": {"type": "string", "description": "The value to save"},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall_preferences",
            "description": "Recall all saved user preferences to personalize the plan. Call this at the START of every planning request.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


# ── Groq API call ──────────────────────────────────────────────────────────────
def call_groq(messages: list, tools: list = None) -> dict:
    import urllib3, time
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    api_key = os.getenv("GROQ_API_KEY", "")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 4096,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    for attempt in range(4):
        resp = requests.post(GROQ_URL, headers=headers, json=payload, verify=False, timeout=60)
        if resp.status_code == 429:
            wait = int(resp.headers.get("retry-after", 20)) + 2
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()

    resp.raise_for_status()
    return resp.json()


# ── TRUE Agentic loop — LLM decides which tools to call ──────────────────────
def run_agent(user_message: str, history: list, status_placeholder) -> str:
    import time

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    tools_used = []
    status_placeholder.info("🤔 Thinking...")

    for iteration in range(12):  # max 12 tool calls per request
        response = call_groq(messages, tools=TOOL_SCHEMAS)
        msg = response["choices"][0]["message"]
        messages.append(msg)

        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            break  # LLM is done calling tools — produce final answer

        for tc in tool_calls:
            name = tc["function"]["name"]
            try:
                args = json.loads(tc["function"]["arguments"])
            except Exception:
                args = {}

            icon = TOOL_ICONS.get(name, "🔧")
            label = name.replace("_", " ").title()
            first_val = list(args.values())[0] if args else ""
            display = f"{first_val}" if first_val else ""
            status_placeholder.info(f"{icon} **{label}**{' → ' + display if display else ''}...")
            tools_used.append(f"{icon} {label}" + (f" ({display})" if display else ""))

            fn = TOOL_MAP.get(name)
            result = fn(**args) if fn else {"error": f"Unknown tool: {name}"}

            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "name": name,
                "content": json.dumps(result, default=str),
            })

        time.sleep(0.5)  # small pause between tool call rounds

    status_placeholder.empty()

    text = msg.get("content") or ""
    if tools_used:
        unique = list(dict.fromkeys(tools_used))
        text += "\n\n---\n*Tools used: " + " · ".join(unique) + "*"

    return text


# ── Guard ─────────────────────────────────────────────────────────────────────
if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY not found in .env file.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ── HERO HEADER (white card) ──────────────────────────────────────────────────
weather_live = bool(os.getenv("OPENWEATHER_API_KEY"))
groq_live = bool(os.getenv("GROQ_API_KEY"))

st.markdown(f"""
<div class="hero-header">
  <div>
    <div class="hero-title">
      <span class="plane-icon">✈️</span>
      <span class="title-text"> AI Travel Agent</span>
    </div>
    <div class="hero-sub" style="animation:titleFadeIn 0.6s ease-out 0.8s both;display:block;">Worldwide &nbsp;·&nbsp; Fully Autonomous &nbsp;·&nbsp; No Follow-up Questions</div>
    <div class="hero-badges" style="animation:titleFadeIn 0.6s ease-out 1s both;">
      <span class="badge">📅 Day-by-day itinerary</span>
      <span class="badge">🌤️ Live weather</span>
      <span class="badge">💰 Budget breakdown</span>
      <span class="badge">🚆 Transport plan</span>
      <span class="badge">🛂 Visa & safety tips</span>
    </div>
  </div>
  <div class="hero-status" style="animation:titleFadeIn 0.6s ease-out 1.1s both;">
    <div style="font-size:12px;font-weight:700;color:#1a3a5c;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.8px;">Live Data Status</div>
    <div class="status-row">{'🟢' if groq_live else '🔴'} AI Brain (Groq · Llama 3.3)</div>
    <div class="status-row">{'🟢' if weather_live else '🟡'} Weather Forecasts</div>
    <div class="status-row">🟡 Flights & Hotels (est.)</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TWO-COLUMN LAYOUT ─────────────────────────────────────────────────────────
chat_col, prompt_col = st.columns([2.8, 1], gap="large")

examples = [
    ("🏰", "10 days Rajasthan, December, ₹60k for 2"),
    ("🗼", "Paris + Swiss Alps, 10 days, couple, mid-range"),
    ("🌏", "Solo Vietnam + Cambodia, 2 weeks, mid-range"),
    ("🗽", "New York + Boston + Washington DC, 10 days"),
    ("🌸", "Japan cherry blossom, first timer, 12 days"),
    ("🦁", "Kenya + Tanzania safari, 10 days, luxury"),
    ("🌺", "Bali honeymoon, 8 days, luxury"),
    ("🏔️", "Machu Picchu + Patagonia, 14 days, adventure"),
    ("🕌", "Morocco — Marrakech + Sahara + Fes, 10 days"),
    ("🐨", "Australia East Coast, 3 weeks, backpacker"),
    ("🎎", "Seoul + Busan, 8 days, K-culture"),
    ("🌴", "Maldives + Sri Lanka, 10 days, luxury"),
]

# ── RIGHT COLUMN — Example prompts ───────────────────────────────────────────
with prompt_col:
    st.markdown("<div class='prompt-panel-title' style='font-size:11px;font-weight:700;color:#74b9ff;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:8px;'>✨ Try these prompts</div>", unsafe_allow_html=True)
    for i, (icon, ex) in enumerate(examples):
        if st.button(f"{icon}  {ex}", key=f"prompt_{i}", use_container_width=True):
            st.session_state["pending_input"] = ex
            st.rerun()
    st.markdown("<p style='font-size:11px;color:#2a4a6a;text-align:center;margin-top:10px;'>Groq · Llama 3.3 · OpenWeatherMap</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_chat"):
        st.session_state["messages"] = []
        st.rerun()

# JS: force dark style on all prompt buttons after Streamlit renders them
st.markdown("""
<script>
function styleButtons() {
    const btns = document.querySelectorAll('button[data-testid="baseButton-secondary"]');
    btns.forEach((btn, i) => {
        btn.style.setProperty('background', '#0d1e30', 'important');
        btn.style.setProperty('border', '1px solid #1e3a55', 'important');
        btn.style.setProperty('border-radius', '11px', 'important');
        btn.style.setProperty('color', '#a8cce8', 'important');
        btn.style.setProperty('text-align', 'left', 'important');
        btn.style.setProperty('min-height', '46px', 'important');
        btn.style.setProperty('white-space', 'normal', 'important');
        btn.style.setProperty('height', 'auto', 'important');
        // Style inner <p> tags
        btn.querySelectorAll('p').forEach(p => p.style.setProperty('color', '#a8cce8', 'important'));
        btn.onmouseenter = () => {
            btn.style.setProperty('background', '#162d48', 'important');
            btn.style.setProperty('border-color', '#4a90d9', 'important');
            btn.style.setProperty('color', '#ffffff', 'important');
            btn.querySelectorAll('p').forEach(p => p.style.setProperty('color', '#ffffff', 'important'));
        };
        btn.onmouseleave = () => {
            btn.style.setProperty('background', '#0d1e30', 'important');
            btn.style.setProperty('border-color', '#1e3a55', 'important');
            btn.style.setProperty('color', '#a8cce8', 'important');
            btn.querySelectorAll('p').forEach(p => p.style.setProperty('color', '#a8cce8', 'important'));
        };
    });
}
// Run immediately and after short delays to catch Streamlit re-renders
styleButtons();
setTimeout(styleButtons, 300);
setTimeout(styleButtons, 800);
setTimeout(styleButtons, 2000);
// Also observe DOM changes
const observer = new MutationObserver(() => styleButtons());
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# ── LEFT COLUMN — Chat ────────────────────────────────────────────────────────
with chat_col:
    has_messages = bool(st.session_state["messages"])

    # Input at TOP when no messages, flows naturally when messages exist
    if not has_messages:
        st.markdown("""
<div style='text-align:center;padding:20px 20px 16px;animation:fadeIn 0.6s ease-out;'>
    <span style='font-size:44px;display:block;margin-bottom:10px;animation:pulse 2s ease-in-out infinite;'>🗺️</span>
    <h3 style='color:#74b9ff;font-size:1.6rem;font-weight:800;margin:0 0 8px;'>Where do you want to go?</h3>
    <p style='color:#6a90b0;font-size:14.5px;max-width:440px;margin:0 auto 16px;line-height:1.7;'>
        Destination · dates · budget · group size — I'll handle the rest.
    </p>
    <div style='display:flex;flex-wrap:wrap;gap:8px;justify-content:center;'>
        <span style='background:rgba(26,115,232,0.15);border:1px solid rgba(26,115,232,0.3);border-radius:20px;padding:4px 12px;font-size:12px;color:#74b9ff;font-weight:600;'>📅 Itinerary</span>
        <span style='background:rgba(108,63,197,0.15);border:1px solid rgba(108,63,197,0.3);border-radius:20px;padding:4px 12px;font-size:12px;color:#a29bfe;font-weight:600;'>🌤️ Live weather</span>
        <span style='background:rgba(232,65,106,0.12);border:1px solid rgba(232,65,106,0.3);border-radius:20px;padding:4px 12px;font-size:12px;color:#fd79a8;font-weight:600;'>💰 Budget</span>
        <span style='background:rgba(26,115,232,0.15);border:1px solid rgba(26,115,232,0.3);border-radius:20px;padding:4px 12px;font-size:12px;color:#74b9ff;font-weight:600;'>🚆 Transport</span>
        <span style='background:rgba(108,63,197,0.15);border:1px solid rgba(108,63,197,0.3);border-radius:20px;padding:4px 12px;font-size:12px;color:#a29bfe;font-weight:600;'>🛂 Visa & safety</span>
    </div>
</div>
""", unsafe_allow_html=True)

    # Render messages
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pending = st.session_state.pop("pending_input", None)
    user_input = st.chat_input("Where to? e.g. '10 days Rajasthan in December, ₹60k for 2 people'") or pending

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            status = st.empty()
            status.info("🤔 Planning your trip...")
            try:
                response_text = run_agent(user_input, st.session_state["messages"][:-1], status)
            except Exception as e:
                status.empty()
                response_text = f"Error: {str(e)}"
            st.markdown(response_text)

        st.session_state["messages"].append({"role": "assistant", "content": response_text})
        st.rerun()
