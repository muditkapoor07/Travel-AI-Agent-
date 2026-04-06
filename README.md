# ✈️ AI Travel Agent — Plan Any Trip, Anywhere

> A fully autonomous, agentic travel planning system that creates complete, executable travel plans for any destination worldwide — without asking follow-up questions.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-orange.svg)](https://groq.com)
[![Neon](https://img.shields.io/badge/Database-Neon%20PostgreSQL-green.svg)](https://neon.tech)

---

## 1. Project Overview

### What It Is
The AI Travel Agent is an autonomous planning agent covering every destination worldwide. Given a vague or detailed travel request, it independently produces a complete, structured, ready-to-book travel plan — including day-by-day itinerary, transport, hotels, budget, weather, visa requirements, and practical tips.

### The Problem It Solves
Planning any trip requires synthesizing dozens of variables simultaneously: weather seasonality, route efficiency, transport options, local ground realities, visa rules, budget trade-offs, and festival calendars. Most travelers either spend hours researching across multiple sources or rely on generic itinerary templates that ignore real constraints.

This agent replaces that entire process with a single natural language input.

### Why It Is Different from Normal AI Chatbots

| Dimension | Normal AI Chatbot | This Agent |
|---|---|---|
| Input | One question at a time | One vague goal |
| Behavior | Responds, waits | Plans autonomously end-to-end |
| Follow-up questions | Many | Zero |
| Output | Text answer | Structured, executable plan |
| Tool usage | Optional / limited | Core to every plan — LLM decides |
| Decision-making | User-driven | Agent-driven |
| Weather awareness | None | Live per-city forecasts |
| Budget optimization | None | Automatic |
| Route logic | None | Geography-aware |
| Memory | None | Persistent across sessions (PostgreSQL) |

---

## 2. What Makes This Agent Autonomous (Agentic Design)

### Goal-Driven Behavior
The agent receives a high-level goal ("10 days Rajasthan, December, ₹60k for 2") and independently decomposes it into sub-tasks: which cities to visit, in what order, by what transport, at what cost, staying where. The user does not manage this decomposition.

### No-Question Autonomous Mode
The agent never asks clarifying questions. If information is missing, it makes reasonable, clearly stated assumptions and proceeds. This is a deliberate design constraint — the agent takes ownership of decisions rather than delegating them back to the user.

### Assumption-Based Decision Making
Every plan begins with an explicit Assumptions section where the agent states what it inferred from the input. This makes the reasoning transparent and correctable, while keeping the execution fully autonomous.

### Multi-Step Planning with True Agentic Tool Loop
The LLM autonomously decides which tools to call, in what order, and how many times — this is not a hardcoded pipeline. The agent:
1. Recalls saved user preferences from persistent database
2. Decides which cities need weather data and fetches them
3. Calls flight and hotel search for each leg
4. Detects new user preferences and saves them automatically
5. Synthesizes all tool results into a final structured plan

### Persistent Memory
The agent remembers user preferences across sessions using Neon PostgreSQL. Every time you plan a trip, it recalls your home city, travel style, budget level, dietary needs, and past preferences — without being asked.

---

## 3. Core Capabilities

### Weather-Aware Planning
Live 5-day forecasts fetched for every destination via OpenWeatherMap API. The agent accounts for monsoon seasons, extreme heat, typhoon risks, and air quality. It will reroute or flag risks without being asked.

### Route and Map Optimization
Routes are optimized using real-world geography — not alphabetical order or tourist popularity. The agent minimizes backtracking, accounts for travel time between cities, and chooses the correct direction of travel (e.g. Jaipur → Jodhpur → Jaisalmer, not the reverse).

### Booking-Aware Recommendations
Every recommendation is framed in terms of bookable components: specific flight legs, train routes, hotel areas (not just city names), and activity categories.

### Budget Estimation and Optimization
Every plan includes an itemized budget table covering transport, accommodation, food, and activities. The agent estimates per-person and total costs, flags where costs can be reduced, and adjusts recommendations when a budget constraint is specified.

### Local, On-Ground Travel Logic
The agent incorporates ground realities that generic tools miss: last-mile connectivity, permit requirements (e.g. Inner Line Permits for Arunachal Pradesh), local festival dates that affect prices and availability, scam-prone areas, cultural norms, and safe vs. risky neighborhoods.

### Visa & Entry Requirements
Every plan includes a dedicated Visa & Entry section with visa type, cost, application method, processing time, and validity — automatically determined per destination.

### Persistent User Memory
The agent saves and recalls user preferences using Neon PostgreSQL. Memory persists across sessions, devices, and Render redeploys. The agent gets more personalized with every interaction.

---

## 4. Tools Used

The agent uses **5 tools** called autonomously by the LLM based on the planning context. It decides which tools to use, when, and how many times.

### `recall_preferences` — User Memory Recall
Reads all saved user preferences from Neon PostgreSQL at the start of every plan. If the user has previously mentioned home city, budget style, dietary needs, or travel interests, the agent retrieves and applies this without asking again.

### `remember_preference` — User Memory Write
Called automatically when the agent detects new information about the user — travel style, budget level, home city, group size, dietary needs, interests. Saves to PostgreSQL using UPSERT. Builds a persistent profile over time.

### `get_weather` — Live Weather Forecasts
Fetches real-time 5-day forecasts via OpenWeatherMap API for every city in the itinerary. Forecast data directly shapes accommodation recommendations, activity timing, and seasonal risk flags.

### `search_flights` — Flight Route Intelligence
Returns route information and realistic fare estimates for a city pair. Called for every flight leg in the itinerary to surface airline options, duration, and INR price ranges.

### `search_hotels` — Hotel Area Recommendations
Returns stay area recommendations and price ranges per city, matched to the user's budget level. Recommends neighborhoods rather than just hotel names — more durable and actionable for booking.

---

## 5. How the Agent Thinks — Execution Flow

```
User Input: "10 days Rajasthan, December, ₹60k for 2"
    │
    ▼
Step 1: LLM receives goal + system prompt
    → Autonomously calls recall_preferences
    → Retrieves saved: home_city=Delhi, travel_style=mid-range

    │
    ▼
Step 2: LLM plans route (Jaipur→Pushkar→Jodhpur→Jaisalmer→Udaipur)
    → Calls get_weather for each city (5 tool calls)
    → December confirmed: 8–20°C, clear skies, ideal

    │
    ▼
Step 3: LLM calls search_flights for each leg
    → DEL→JAI, UDR→DEL
    → Receives route info and fare estimates

    │
    ▼
Step 4: LLM calls search_hotels for each city
    → Matched to mid-range budget
    → Receives area recommendations + nightly price ranges

    │
    ▼
Step 5: LLM detects "₹60k budget" preference
    → Calls remember_preference(budget_level, mid-range)
    → Saved to Neon PostgreSQL for future trips

    │
    ▼
Step 6: LLM synthesizes all tool results → produces plan
    → 9-section structured output
    → Budget table using actual estimates
    → Weather section using live forecast data
    → Visa section auto-included

Output: Complete executable plan
Sections: Assumptions · Itinerary · Transport · Hotels ·
          Budget · Weather · Visa & Entry · Practical Tips
Footer:   All tools used listed with call details
```

---

## 6. Example Use Cases

### "10 days Rajasthan, December, ₹60k for 2"
Jaipur → Pushkar → Jodhpur → Jaisalmer → Udaipur. One-directional route, sleeper trains, mid-range havelis, live weather confirmation, itemized budget within ₹60k.

### "Solo Vietnam + Cambodia, 2 weeks, mid-range"
Hanoi → Hoi An → Ho Chi Minh City → Siem Reap → Phnom Penh. Optimized route, Vietnam e-visa + Cambodia e-visa instructions, live weather per city, mid-range hotel areas.

### "Kerala family trip, April, 4 people"
Kochi → Munnar → Alleppey → Kovalam. April heat flag noted, houseboat recommendation, family-appropriate stays, budget table for 4.

### "Japan cherry blossom, first timer, 12 days"
Tokyo → Nikko → Kyoto → Osaka → Hiroshima. Bloom window timing, JR Pass recommendation, live weather forecasts, visa-free entry for most nationalities confirmed.

### "Northeast India — Meghalaya + Arunachal, 10 days"
Inner Line Permit flagged automatically, Guwahati gateway, Shillong → Cherrapunji → Tawang, road condition realities included.

### "Bali honeymoon, 8 days, luxury"
Ubud → Seminyak → Nusa Dua. Private villa recommendations, luxury tier matching, live weather, Bali entry requirements.

---

## 7. What the User Can Do

### Inputs — what to include
- Destination or region
- Duration or travel dates / season
- Budget (total or per day, per person)
- Group composition (solo, couple, family, group size)
- Travel style (budget, mid-range, luxury, adventure)
- Any hard constraints (must-visit places, avoid certain areas)

Everything else is handled by the agent.

### Outputs — what you receive
- **Assumptions** — what the agent inferred
- **Day-by-day Itinerary** — specific activities per day, per city
- **Transport Plan** — flights, trains, buses with route recommendations
- **Stay Areas & Hotels** — recommended neighborhoods and hotel tiers
- **Budget Estimate** — itemized table with per-category and total costs
- **Weather Summary** — live forecast data for each destination
- **Visa & Entry Requirements** — type, cost, application process, duration
- **Practical Tips** — safety, scams, cultural norms, packing

---

## 8. Non-Goals — What This Agent Does NOT Do

- No conversational small talk
- No repeated clarification questions
- No generic travel-blog advice
- No real-time booking execution
- No single-destination Q&A

---

## 9. Architecture — High Level

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│         Streamlit Web App — Dark theme, animated UI      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              TRUE Agentic Tool Loop                      │
│                                                          │
│  LLM (Groq · Llama 3.3 70B) autonomously decides:       │
│                                                          │
│  1. recall_preferences  → Neon PostgreSQL               │
│  2. get_weather         → OpenWeatherMap API            │
│  3. search_flights      → Knowledge-based estimates     │
│  4. search_hotels       → Knowledge-based estimates     │
│  5. remember_preference → Neon PostgreSQL               │
│                                                          │
│  Loop continues until LLM signals completion             │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Structured 9-Section Output                 │
│      Rendered as markdown in Streamlit chat              │
└─────────────────────────────────────────────────────────┘

Persistent Storage:
  Neon PostgreSQL ──► user_preferences table
                      Survives redeploys, restarts, scaling
```

---

## 10. Why This Is Not a Chatbot

| Characteristic | Chatbot | This Agent |
|---|---|---|
| Interaction model | Turn-by-turn Q&A | Single input → complete plan |
| Decision ownership | User decides | Agent decides, user reviews |
| Follow-up questions | Frequent | Zero by design |
| Tool usage | Rare | Core — LLM drives tool selection |
| Output structure | Freeform text | Fixed, actionable 9 sections |
| Route optimization | Never | Always, geography-aware |
| Budget enforcement | Never | Automatic |
| Weather integration | Never | Live data per city |
| Memory | Session only | Persistent PostgreSQL |
| Visa/permit logic | Generic if asked | Automatic per destination |
| Assumption handling | Asks user | States assumptions, proceeds |

---

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Llama 3.3 70B via Groq API |
| Agent Loop | Groq native function calling |
| Weather | OpenWeatherMap API |
| Memory | Neon PostgreSQL (persistent, serverless) |
| Language | Python 3.11+ |
| Deployment | Render (Web Service) |

---

## Agent Capabilities

| Capability | Status |
|---|---|
| Autonomous planning (no questions) | ✅ |
| Assumption-based decision making | ✅ |
| Multi-constraint optimization | ✅ |
| Live weather per city | ✅ |
| LLM-directed tool selection | ✅ |
| Dynamic multi-turn tool loop | ✅ |
| Persistent memory across sessions | ✅ PostgreSQL |
| Real flight/hotel data | 🟡 Knowledge-based estimates |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | From console.groq.com |
| `OPENWEATHER_API_KEY` | Yes | From openweathermap.org |
| `DATABASE_URL` | Yes | Neon PostgreSQL connection string |
| `PYTHON_VERSION` | Render only | Set to `3.11.0` |

---

## Running Locally

```bash
git clone https://github.com/muditkapoor07/Travel-AI-Agent-.git
cd Travel-AI-Agent-
pip install -r requirements.txt

# Create .env file with your keys
# GROQ_API_KEY=...
# OPENWEATHER_API_KEY=...
# DATABASE_URL=postgresql://...

streamlit run app.py
```

---

## Deploying to Render

1. Push to GitHub
2. Go to **render.com** → New → Web Service
3. Connect `muditkapoor07/Travel-AI-Agent-` repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.headless true --server.enableCORS false`
   - **Region:** Singapore
5. Add environment variables: `GROQ_API_KEY`, `OPENWEATHER_API_KEY`, `DATABASE_URL`, `PYTHON_VERSION`
6. Deploy — `render.yaml` handles the rest

---

*Built with Groq · Llama 3.3 · OpenWeatherMap · Neon PostgreSQL · Streamlit*
