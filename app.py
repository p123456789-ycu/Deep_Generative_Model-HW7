import gradio as gr

from rag import WorldCupRAG
from orchestrator import run_all_agents
from image_generator import generate_image
from llm_agent import generate_image_prompt
from landmark_fetcher import fetch_landmark

rag = WorldCupRAG()


def run_agent(
    city,
    travel_date,
    days,
    budget,
    travel_type,
    interests
):
    interest_text = ", ".join(interests)

    query = f"""
    {city}
    World Cup 2026
    {travel_date}
    {interest_text}
    """

    context = rag.retrieve(query)

    itinerary, food, budget_plan = run_all_agents(
        city=city,
        days=days,
        budget=budget,
        travel_type=travel_type,
        interests=interest_text,
        travel_date=travel_date,
        context=context
    )

    landmark = fetch_landmark(city)

    combined = f"{itinerary}\n{food}"
    image_prompt = generate_image_prompt(city, combined)
    poster = generate_image(image_prompt, landmark)

    return context, itinerary, food, budget_plan, landmark, poster


with gr.Blocks(title="⚽ FIFA World Cup 2026 Travel Agent") as demo:

    gr.Markdown("""
# ⚽ FIFA World Cup 2026 Travel Agent

Plan your FIFA World Cup 2026 journey using:
✓ RAG Knowledge Base &nbsp; ✓ Multi-Agent LLM &nbsp; ✓ ControlNet Image Generation
""")

    with gr.Row():
        with gr.Column(scale=1):
            city = gr.Dropdown(
                [
                    "New York City", "Los Angeles", "Dallas",
                    "San Francisco", "Seattle", "Atlanta",
                    "Miami", "Houston", "Kansas City",
                    "Philadelphia", "Boston", "Mexico City",
                    "Guadalajara", "Monterrey", "Toronto", "Vancouver"
                ],
                value="New York City",
                label="🏟️ World Cup Host City"
            )
            travel_date = gr.Textbox(
                value="2026-07-19",
                label="📅 Travel Date"
            )
            days = gr.Slider(
                minimum=1, maximum=14, value=5, step=1,
                label="🗓️ Trip Duration (Days)"
            )
            budget = gr.Radio(
                ["Budget", "Medium", "Luxury"],
                value="Medium",
                label="💰 Budget Level"
            )
            travel_type = gr.Radio(
                ["Solo", "Couple", "Friends", "Family"],
                value="Friends",
                label="👥 Travel Type"
            )
            interests = gr.CheckboxGroup(
                choices=[
                    "Football", "Food", "Nightlife", "Shopping",
                    "Museums", "Photography", "Nature",
                    "Theme Parks", "Local Culture", "Architecture"
                ],
                value=["Football", "Food"],
                label="🎯 Interests"
            )
            btn = gr.Button("🚀 Generate My Trip", variant="primary")

    with gr.Tabs():

        with gr.Tab("🗺️ Itinerary"):
            itinerary_out = gr.Textbox(label="Day-by-Day Itinerary", lines=20)

        with gr.Tab("🍜 Food Guide"):
            food_out = gr.Textbox(label="Food & Dining Recommendations", lines=20)

        with gr.Tab("💰 Budget Plan"):
            budget_out = gr.Textbox(label="Budget Breakdown", lines=20)

        with gr.Tab("🖼️ Travel Poster"):
            with gr.Row():
                landmark_out = gr.Image(label="🏙️ City Landmark (ControlNet Input)")
                poster_out = gr.Image(label="🎨 AI Generated Poster (ControlNet Output)")

        with gr.Tab("📚 RAG Knowledge"):
            context_out = gr.Textbox(label="Retrieved Knowledge", lines=12)

    btn.click(
        fn=run_agent,
        inputs=[city, travel_date, days, budget, travel_type, interests],
        outputs=[context_out, itinerary_out, food_out, budget_out, landmark_out, poster_out]
    )

demo.launch()
