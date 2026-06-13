import requests

OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

def generate_plan(
    city,
    days,
    budget,
    travel_type,
    interests,
    travel_date,
    context
):

    prompt = f"""
You are a FIFA World Cup 2026 Travel Planning Agent.

Host City:
{city}

Travel Date:
{travel_date}

Trip Length:
{days} days

Budget:
{budget}

Travel Type:
{travel_type}

Interests:
{interests}

Retrieved Knowledge:
{context}

Create a detailed travel plan.

Include:

1. Day-by-day itinerary
2. World Cup activities
3. Stadium recommendations
4. Tourist attractions
5. Local food
6. Transportation
7. Estimated budget
8. Travel tips

Use markdown format.

Use retrieved knowledge as factual information.
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


def generate_image_prompt(
    city,
    itinerary
):

    prompt = f"""
Create a Stable Diffusion prompt.

Theme:
FIFA World Cup 2026

Location:
{city}

Travel Plan:
{itinerary}

Requirements:

- FIFA World Cup 2026
- football atmosphere
- stadium
- football fans
- city skyline
- travel poster
- tourism advertisement
- ultra realistic
- cinematic lighting
- 8k
- highly detailed
- vibrant colors

Return ONLY the final image prompt.
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
