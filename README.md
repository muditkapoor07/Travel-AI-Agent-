# ✈️ AI Travel Agent — India & Asia

> A fully autonomous, agentic travel planning system that creates complete, executable travel plans without asking follow-up questions.

---

## 1. Project Overview

### What It Is
The AI Travel Agent is an autonomous planning agent built for India and Asian countries. Given a vague or detailed travel request, it independently produces a complete, structured, ready-to-book travel plan — including day-by-day itinerary, transport, hotels, budget, weather, visa requirements, and practical tips.

### The Problem It Solves
Planning a trip across India or Asia requires synthesizing dozens of variables simultaneously: weather seasonality, route efficiency, transport options, local ground realities, visa rules, budget trade-offs, and festival calendars. Most travelers either spend hours researching across multiple sources or rely on generic itinerary templates that ignore real constraints.

This agent replaces that entire process with a single natural language input.

### Why It Is Different from Normal AI Chatbots

Most AI systems (including GPT-based chatbots) respond to one question at a time, require the user to guide the conversation, and produce generic answers. This agent operates differently:

| Dimension | Normal AI Chatbot | This Agent |
|---|---|---|
| Input | One question at a time | One vague goal |
| Behavior | Responds, waits | Plans autonomously end-to-end |
| Follow-up questions | Many | Zero |
| Output | Text answer | Structured, executable plan |
| Tool usage | Optional / limited | Core to every plan |
| Decision-making | User-driven | Agent-driven |
| Weather awareness | None | Built-in, automatic |
| Budget optimization | None | Automatic |
| Route logic | None | Geography-aware |

---

## 2. What Makes This Agent Autonomous (Agentic Design)

### Goal-Driven Behavior
The agent receives a high-level goal ("10 days Rajasthan, December, ₹60k for 2") and independently decomposes it into sub-tasks: which cities to visit, in what order, by what transport, at what cost, staying where. The user does not manage this decomposition.

### No-Question Autonomous Mode
The agent never asks clarifying questions. If information is missing, it makes reasonable, clearly stated assumptions and proceeds. This is a deliberate design constraint — the agent takes ownership of decisions rather than delegating them back to the user.

### Assumption-Based Decision Making
Every plan begins with an explicit Assumptions section where the agent states what it inferred from the input. This makes the reasoning transparent and correctable, while keeping the execution fully autonomous.

### Multi-Step Planning and Self-Correction
The agent does not produce a single-pass answer. It:
1. Fetches real-time data (weather, etc.)
2. Reasons about routes and feasibility
3. Builds a structured plan
4. Cross-checks against budget and time constraints
5. Adjusts and optimizes before producing output

### Tool-Based Execution Loop
The agent uses external tools as part of its reasoning process — not as optional lookups, but as required inputs to every plan. Weather data, route logic, and budget calculations are all grounded in tool outputs before the final plan is written.

---

## 3. Core Capabilities

### Weather-Aware Planning
The agent automatically fetches live 5-day forecasts for every destination in the itinerary. It accounts for monsoon seasons, extreme heat, typhoon risks, and air quality when recommending travel windows. It will reroute or flag risks without being asked.

### Route and Map Optimization
Routes are optimized using real-world geography — not alphabetical order or tourist popularity. The agent minimizes backtracking, accounts for travel time between cities, and chooses the correct direction of travel (e.g. Jaipur → Jodhpur → Jaisalmer, not the reverse).

### Booking-Aware Recommendations
The agent thinks in terms of bookable components: specific flight legs, train numbers, hotel areas (not just city names), and activity categories. Every recommendation is framed in terms of what the traveler would actually search for when booking.

### Budget Estimation and Optimization
Every plan includes an itemized budget table covering transport, accommodation, food, and activities. The agent estimates per-person and total costs, flags where costs can be reduced, and adjusts recommendations when a budget constraint is specified.

### Local, On-Ground Travel Logic
The agent incorporates ground realities that generic itinerary tools miss: last-mile connectivity, permit requirements (e.g. Inner Line Permits for Arunachal Pradesh), local festival dates that affect prices and availability, scam-prone areas, cultural norms, and safe vs. risky neighborhoods for stays.

### Risk Avoidance
The agent proactively avoids problematic scenarios — monsoon-flooded routes, typhoon-season beach destinations, extreme summer heat in the Thar Desert — without the user needing to specify these constraints.

---

## 4. Tools Used

The agent uses **5 tools** that it calls autonomously based on the planning context. It decides which tools to use, when to use them, and in what order — without any hardcoded pipeline.

### `recall_preferences` — User Memory Recall
**What:** Reads saved user preferences from persistent local storage.
**Why:** Called at the start of every plan. If the user has previously mentioned their home city, budget style, dietary needs, or travel interests, the agent retrieves this and uses it to personalize the plan without asking again.

### `remember_preference` — User Memory Write
**What:** Saves a user preference (key-value) to persistent storage.
**Why:** Called automatically when the agent detects new information about the user — travel style, budget level, home city, group composition, interests. Builds a profile over time, making every subsequent plan more accurate.

### `get_weather` — Live Weather Forecasts
**What:** Fetches real-time 5-day forecasts via OpenWeatherMap API.
**Why:** Travel planning is fundamentally seasonal. The agent calls this for every city in the itinerary — not as an optional lookup but as a required input. Forecast data directly shapes accommodation recommendations, activity timing, and risk flags.

### `search_flights` — Flight Route Intelligence
**What:** Returns route information and fare estimates for a city pair.
**Why:** Every flight leg in the itinerary is explicitly reasoned about. The agent calls this per leg to surface airline options, duration, and realistic INR price ranges — grounding the transport plan in bookable reality.

### `search_hotels` — Hotel Area Recommendations
**What:** Returns stay area recommendations and price ranges per city.
**Why:** Called for every city in the itinerary matched to the user's budget level. The agent recommends neighborhoods, not just hotel names — which is more durable and actionable for actual booking.

### Budget Calculation Logic
**What:** Structured cost estimation across transport, accommodation, food, and activities — built into the LLM's reasoning, not a separate API.
**Why:** Budget is the most common constraint users have. The agent builds itemized markdown tables showing per-category and total costs, and adjusts recommendations when a budget constraint is specified.

### Geography and Route Reasoning
**What:** Built-in spatial reasoning about distances, transport options, and route sequencing — part of the LLM's knowledge.
**Why:** India and Asia have complex, non-obvious transport networks. The agent knows that Varanasi is best reached by train from Delhi, that Meghalaya requires a connection through Guwahati, and that Bangkok to Chiang Mai has flight and overnight train options at different price points.

---

## 5. How the Agent Thinks — Execution Flow

```
User Input: "10 days Rajasthan, December, ₹60k for 2"
    │
    ▼
Step 1: LLM receives goal + system prompt
    → Autonomously decides to call recall_preferences first
    → Retrieves: home_city=Delhi, travel_style=mid-range (if previously saved)

    │
    ▼
Step 2: LLM decides route (Jaipur→Pushkar→Jodhpur→Jaisalmer→Udaipur)
    → Autonomously calls get_weather for each city
    → Receives live 5-day forecasts
    → December confirmed: 8-20°C, clear skies, ideal season

    │
    ▼
Step 3: LLM calls search_flights for each flight leg
    → DEL→JAI, UDR→DEL
    → Receives route info and fare estimates

    │
    ▼
Step 4: LLM calls search_hotels for each city
    → Matches to mid-range budget level
    → Receives area recommendations and nightly price ranges

    │
    ▼
Step 5: LLM detects "mid-range" preference → calls remember_preference
    → Saves: budget_level=mid-range for future trips

    │
    ▼
Step 6: LLM has all data — produces structured plan
    → Assembles 9-section output grounded in tool results
    → Budget table using actual hotel/transport estimates
    → Weather section using live forecast data
    → Visa section (e-Tourist Visa if international)

    │
    ▼
Output: Complete, executable travel plan
    Sections: Assumptions · Itinerary · Transport · Hotels ·
              Budget · Weather · Visa & Entry · Practical Tips
    Footer: Tools used listed with call details
```

---

## 6. Example Use Cases

### "Plan a 7-day Vietnam trip, mid-range budget"
The agent selects Hanoi → Hoi An → Ho Chi Minh City, optimizes the route to avoid backtracking, recommends the correct flight legs, provides live weather for each city, estimates costs at the mid-range level, and includes Vietnam e-visa instructions.

### "Optimize budget travel across Rajasthan, ₹40k for 2, December"
The agent selects Jaipur → Pushkar → Jodhpur → Jaisalmer → Udaipur (one-directional route), recommends sleeper trains over flights to stay within budget, identifies budget guesthouse areas in each city, and produces a day-by-day plan within the stated constraint.

### "Avoid monsoon while planning Southeast Asia, 2 weeks"
The agent checks current month against monsoon calendars for Thailand, Vietnam, Cambodia, and Indonesia. It routes the trip to avoid wet-season destinations and suggests the correct sub-regions (e.g. east coast Vietnam vs. west coast during different months).

### "Northeast India — Meghalaya + Arunachal, adventure, 10 days"
The agent flags the Inner Line Permit requirement for Arunachal Pradesh, recommends the Guwahati gateway, sequences the route correctly (Shillong → Cherrapunji → Tawang), and notes road condition realities for the remote mountain routes.

### "Bali honeymoon, 8 days, luxury"
The agent recommends Ubud (culture, rice terraces) → Seminyak (beach, nightlife) → Nusa Dua (luxury resorts), matches accommodation to luxury tier, includes villa options, and provides current weather and Bali entry requirements.

---

## 7. What the User Can Do

### Inputs
Users provide a natural language description of their trip. Useful elements to include:
- Destination or region
- Duration or travel dates
- Budget (total or per day, per person)
- Group composition (solo, couple, family, group size)
- Travel style (budget, mid-range, luxury, adventure)
- Any hard constraints (must-visit places, avoid certain regions)

Everything else is handled by the agent.

### Outputs
Every response includes:
- **Assumptions** — what the agent inferred from the input
- **Day-by-day Itinerary** — specific activities per day, per city
- **Transport Plan** — flights, trains, buses with specific route recommendations
- **Stay Areas & Hotels** — recommended neighborhoods and hotel tiers
- **Budget Estimate** — itemized table with per-category and total costs
- **Weather Summary** — live forecast data for each destination
- **Visa & Entry Requirements** — type, cost, application process, duration
- **Practical Tips** — safety, scams, cultural norms, packing

### What the Agent Handles Automatically
- City sequencing and route direction
- Transport mode selection
- Weather risk assessment
- Budget constraint management
- Permit and visa identification
- Festival and peak season awareness
- Local ground realities

---

## 8. Non-Goals — What This Agent Does NOT Do

- **No conversational small talk** — the agent does not engage in general chat
- **No repeated clarification questions** — missing information is inferred, not requested
- **No generic advice** — every plan is specific to the stated destination and constraints
- **No real-time booking** — the agent recommends bookable components but does not execute bookings
- **No opinion-based travel blogging** — outputs are structured and decision-focused, not narrative
- **No single-destination Q&A** — the agent is designed for multi-city, multi-constraint planning tasks

---

## 9. Architecture — High Level

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│              Streamlit Web App (app.py)                  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    LLM Reasoning Engine                  │
│         Groq API — Llama 3.3 70B Versatile              │
│                                                          │
│  System Prompt: Autonomous travel agent persona,         │
│  decision rules, output format, formatting constraints   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              TRUE Agentic Tool Loop                      │
│   LLM autonomously decides which tools to call           │
│                                                          │
│   recall_preferences → get_weather (per city)            │
│   → search_flights (per leg) → search_hotels (per city) │
│   → remember_preference (if new info detected)           │
│                                                          │
│   Loop repeats until LLM signals completion              │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Structured Output                       │
│   9-section markdown plan rendered in Streamlit chat     │
└─────────────────────────────────────────────────────────┘

External APIs & Storage:
  OpenWeatherMap  ──► Live 5-day forecasts per city
  Groq API        ──► LLM inference (low latency)
  user_memory.json ─► Persistent user preferences (local)
```

**Key design decisions:**
- The LLM **autonomously decides** which tools to call, in what order, and how many times — this is a true agentic loop, not a hardcoded pipeline
- `recall_preferences` is called at the start of every plan — the agent personalizes every response based on what it has learned about the user
- `remember_preference` is called automatically when the user mentions travel style, budget level, home city, dietary needs, or group size
- Memory persists across sessions in `user_memory.json` — the agent gets smarter with each interaction
- All API calls use `verify=False` to handle corporate SSL proxy environments
- Retry logic with `retry-after` header handling manages Groq rate limits automatically

---

## 10. Why This Is Not a Chatbot

| Characteristic | Chatbot | This Agent |
|---|---|---|
| **Interaction model** | Turn-by-turn Q&A | Single input → complete plan |
| **Decision ownership** | User decides everything | Agent decides, user reviews |
| **Follow-up questions** | Frequent | Zero by design |
| **Tool usage** | Rare or cosmetic | Core to every plan |
| **Output structure** | Freeform text | Fixed, actionable sections |
| **Route optimization** | Never | Always |
| **Budget enforcement** | Never | Automatic |
| **Weather integration** | Never | Live data per city |
| **Assumption handling** | Asks user | States assumptions, proceeds |
| **Visa/permit logic** | Generic if asked | Automatic per destination |
| **Ground-level logic** | Tourist-blog level | Operational detail |
| **Failure mode** | Asks more questions | Infers and flags uncertainty |

A chatbot is a reactive system. This agent is a proactive planning system that takes ownership of a complex, multi-variable problem and delivers a complete, optimized output.

---

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Llama 3.3 70B via Groq API |
| Agent Loop | Groq native function calling — LLM drives tool selection |
| Weather | OpenWeatherMap API (live 5-day forecasts) |
| Memory | JSON file — persistent user preference store |
| Language | Python 3.11+ |
| Deployment | Render (Web Service) |

---

## Agent Capabilities — Updated Status

| Capability | Status |
|---|---|
| Autonomous planning (no questions) | ✅ |
| Assumption-based decision making | ✅ |
| Multi-constraint optimization | ✅ |
| Live weather per city | ✅ |
| LLM-directed tool selection | ✅ |
| Dynamic multi-turn tool loop | ✅ |
| Persistent user memory across sessions | ✅ |
| Real flight/hotel data | 🟡 Knowledge-based estimates |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Groq API key from console.groq.com |
| `OPENWEATHER_API_KEY` | Recommended | OpenWeatherMap key from openweathermap.org |

---

## Running Locally

```bash
git clone https://github.com/muditkapoor07/Travel-AI-Agent-.git
cd Travel-AI-Agent-
pip install -r requirements.txt
# Add your keys to .env
streamlit run app.py
```

---

## Deploying to Render

1. Push to GitHub
2. Connect repo at render.com → New Web Service
3. Add environment variables: `GROQ_API_KEY`, `OPENWEATHER_API_KEY`
4. Deploy — `render.yaml` handles the rest

---

*Built with Groq · Llama 3.3 · OpenWeatherMap · Streamlit*
