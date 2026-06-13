import os
import wikipediaapi

# =====================================
# Create folders
# =====================================

os.makedirs("kb", exist_ok=True)
os.makedirs("kb/cities", exist_ok=True)

# =====================================
# Wikipedia
# =====================================

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="WorldCupTravelAgent/1.0"
)

# =====================================
# Host cities
# =====================================

HOST_CITIES = {
    "New York City": {
        "stadium": "MetLife Stadium",
        "country": "USA",
        "special": "2026 FIFA World Cup Final Host"
    },

    "Los Angeles": {
        "stadium": "SoFi Stadium",
        "country": "USA",
        "special": "Major host city"
    },

    "Dallas": {
        "stadium": "AT&T Stadium",
        "country": "USA",
        "special": "Major host city"
    },

    "San Francisco": {
        "stadium": "Levi's Stadium",
        "country": "USA",
        "special": "Bay Area host city"
    },

    "Seattle": {
        "stadium": "Lumen Field",
        "country": "USA",
        "special": "Pacific Northwest host city"
    },

    "Atlanta": {
        "stadium": "Mercedes-Benz Stadium",
        "country": "USA",
        "special": "Southern USA host city"
    },

    "Miami": {
        "stadium": "Hard Rock Stadium",
        "country": "USA",
        "special": "Florida host city"
    },

    "Houston": {
        "stadium": "NRG Stadium",
        "country": "USA",
        "special": "Texas host city"
    },

    "Kansas City": {
        "stadium": "Arrowhead Stadium",
        "country": "USA",
        "special": "Midwest host city"
    },

    "Philadelphia": {
        "stadium": "Lincoln Financial Field",
        "country": "USA",
        "special": "East Coast host city"
    },

    "Boston": {
        "stadium": "Gillette Stadium",
        "country": "USA",
        "special": "New England host city"
    },

    "Mexico City": {
        "stadium": "Estadio Azteca",
        "country": "Mexico",
        "special": "Opening Match Host"
    },

    "Guadalajara": {
        "stadium": "Estadio Akron",
        "country": "Mexico",
        "special": "Mexico host city"
    },

    "Monterrey": {
        "stadium": "Estadio BBVA",
        "country": "Mexico",
        "special": "Mexico host city"
    },

    "Toronto": {
        "stadium": "BMO Field",
        "country": "Canada",
        "special": "Canada host city"
    },

    "Vancouver": {
        "stadium": "BC Place",
        "country": "Canada",
        "special": "Canada host city"
    }
}

# =====================================
# World Cup Schedule
# =====================================

schedule_text = """
FIFA World Cup 2026

Tournament Dates:
June 11, 2026 - July 19, 2026

Group Stage:
June 11 - June 27
72 matches

Round of 32:
June 28 - July 3
16 matches

Round of 16:
July 4 - July 7
8 matches

Quarterfinals:
July 9 - July 11
4 matches

Semifinals:
July 14 - July 15
2 matches

Third Place Match:
July 18

Final:
July 19

Final Venue:
MetLife Stadium
New York / New Jersey
USA

Host Countries:
United States
Canada
Mexico

Teams:
48

Matches:
104
"""

with open(
    "kb/worldcup_schedule.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(schedule_text)

print("Created worldcup_schedule.txt")

# =====================================
# Generate city knowledge files
# =====================================

for city, info in HOST_CITIES.items():

    print(f"Generating {city}...")

    page = wiki.page(city)

    summary = ""

    if page.exists():
        summary = page.summary[:4000]
    else:
        summary = f"{city} is a FIFA World Cup 2026 host city."

    content = f"""
CITY: {city}

COUNTRY:
{info['country']}

WORLD CUP STADIUM:
{info['stadium']}

WORLD CUP NOTE:
{info['special']}

CITY OVERVIEW:
{summary}

TRAVEL RECOMMENDATIONS:
- Explore local attractions
- Experience local cuisine
- Visit the World Cup stadium
- Use public transportation
- Attend FIFA World Cup events

BEST FOR:
- Football Fans
- Tourism
- Food
- Photography
"""

    filename = city.lower()
    filename = filename.replace(" ", "_")

    filepath = f"kb/cities/{filename}.txt"

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)

print("\nKnowledge Base Generated Successfully!")