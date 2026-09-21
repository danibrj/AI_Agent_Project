from AI_agent.client import get_client
import sys

sys.stdout.reconfigure(encoding="utf-8")

client = get_client()

async def run_agent(message):
     
    messages = [
        {
            "role" : "system",
            "content" : """
                you are a AI Assistant and you should give helpful answer
            """
        },
        {
            "role": "user",
            "content": message
        }
    ]
     
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages= messages
    )
    
    answer = response.choices[0].message
    
    return answer.content
