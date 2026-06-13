import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def run(city, days, travel_type, interests, travel_date, context):

    prompt = f"""
You are a FIFA World Cup 2026 Itinerary Planning Agent.
Your ONLY job is to create a day-by-day travel itinerary.

Host City: {city}
Travel Date: {travel_date}
Trip Length: {days} days
Travel Type: {travel_type}
Interests: {interests}

Retrieved Knowledge:
{context}

Create a detailed day-by-day itinerary.

Include:
- Morning / Afternoon / Evening schedule
- World Cup match viewing suggestions
- Stadium visit recommendations
- Key tourist attractions
- Local transportation tips

Use markdown format.
Do NOT include food recommendations or budget breakdown (other agents handle that).
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
