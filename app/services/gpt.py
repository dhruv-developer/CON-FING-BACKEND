import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize Perplexity-compatible OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.perplexity.ai"
)

async def generate_report(user_id: str, activity: dict, anomaly_score: float, deviant_features: dict) -> str:
    prompt = (
        f"You are a digital forensics expert. Analyze this anomaly:\n"
        f"User: {user_id}\n"
        f"New behavior: {activity}\n"
        f"Anomaly score: {anomaly_score:.2f}\n"
        f"Deviant features: {deviant_features}\n\n"
        f"Explain this in a concise forensic report with cause, significance, and recommended action."
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a digital forensics assistant. Generate concise, detailed forensic reports "
                "based on anomaly data and user behavior patterns."
            ),
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # Non-streaming completion
    response = client.chat.completions.create(
        model="sonar-pro",  # You can change to gpt-3.5-turbo if needed
        messages=messages
    )

    return response.choices[0].message.content.strip()
