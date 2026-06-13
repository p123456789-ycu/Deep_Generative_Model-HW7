import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def run(city, days, budget, travel_type, context):

    prompt = f"""
You are a FIFA World Cup 2026 Budget Planning Agent.
Your ONLY job is to estimate travel costs and provide budget advice.

Host City: {city}
Trip Length: {days} days
Budget Level: {budget}
Travel Type: {travel_type}

Retrieved Knowledge:
{context}

Create a detailed budget breakdown.

Include:
- Estimated daily cost (USD)
- Accommodation cost range
- Transportation cost
- Match ticket price range
- Food & drinks budget
- Activities & attractions budget
- Total estimated trip cost
- Money-saving tips

Use markdown format with a cost table.
Do NOT include itinerary schedule or food recommendations (other agents handle that).
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
