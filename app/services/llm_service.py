import os
import asyncio

from groq import Groq

from dotenv import load_dotenv


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



async def generate_summary(
    text: str
):

    prompt = f"""

    Summarize the following PDF content
    into concise professional notes.

    PDF Content:

    {text}
    only answer in 1k words and only bulleted points.
    """

    response = await asyncio.to_thread(
        client.chat.completions.create,
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
