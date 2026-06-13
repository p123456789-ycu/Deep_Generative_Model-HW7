import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def run(city, days, budget, interests, context):

    prompt = f"""
You are a FIFA World Cup 2026 Food & Dining Agent.
Your ONLY job is to recommend food and restaurants.

Host City: {city}
Trip Length: {days} days
Budget Level: {budget}
Interests: {interests}

Retrieved Knowledge:
{context}

Create a detailed food and dining guide.

Include:
- Must-try local dishes
- Restaurant recommendations by budget
- Street food and local markets
- Food near stadiums (match day eating)
- Breakfast / Lunch / Dinner suggestions

Use markdown format.
Do NOT include itinerary schedule or budget breakdown (other agents handle that).
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
