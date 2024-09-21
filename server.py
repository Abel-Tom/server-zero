import asyncio
import os

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

from main import initialize, server_chat

app = FastAPI()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    message: str  
    refresh: bool

class Payload(BaseModel):
    message: str  




@app.get("/")
def read_root():
    return {"Hello": "World"}

async def data_generator():
    for i in range(10):
        yield f"Data chunk {i}\n"
        await asyncio.sleep(1)

@app.post("/")
def create_item(query: Payload) -> str:
    agent = initialize()
    result = server_chat(agent, query)
    if result:
        print('result ', result)
        return result
    else:
        raise HTTPException(status_code=500, detail="Error processing item")

@app.get("/dir")
async def get_dir(folder: str):
    folder_name = ''
    if folder:
        folder_name = folder[1:]
    folder_path = os.path.join(os.getcwd(), folder_name)

    if os.path.exists(folder_path):
        for root, folders, files in os.walk(folder_path):
            return {
                "files": files,
                "folders": folders
            }
    else:
        raise HTTPException(status_code=400, detail="Folder does not exist")
    


@app.post("/stream")
async def stream_data(payload: Payload):
    agent = initialize()
    chain, prompt = agent.get_chain()
    return StreamingResponse(server_chat(agent, payload.message, chain, prompt) , media_type="text/plain")

