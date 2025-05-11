from fastapi import FastAPI

import openai
import uvicorn

from config import OPENAI_API_KEY


app = FastAPI()

openai.api_key = OPENAI_API_KEY

@app.get("/story/{prompt}")
async def get_story(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return {"story": response.choices[0].message["content"]}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
