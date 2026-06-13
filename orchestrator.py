from concurrent.futures import ThreadPoolExecutor, as_completed

from agents import itinerary_agent, food_agent, budget_agent


def run_all_agents(
    city,
    days,
    budget,
    travel_type,
    interests,
    travel_date,
    context
):
    results = {
        "itinerary": "",
        "food": "",
        "budget": ""
    }

    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = {
            executor.submit(
                itinerary_agent.run,
                city, days, travel_type, interests, travel_date, context
            ): "itinerary",

            executor.submit(
                food_agent.run,
                city, days, budget, interests, context
            ): "food",

            executor.submit(
                budget_agent.run,
                city, days, budget, travel_type, context
            ): "budget"
        }

        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = f"Error: {e}"

    return (
        results["itinerary"],
        results["food"],
        results["budget"]
    )
