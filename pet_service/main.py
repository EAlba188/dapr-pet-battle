from fastapi import FastAPI
from pydantic import BaseModel
from dapr.clients.grpc.client import DaprGrpcClient as DaprClient
import uuid
import json

app = FastAPI()


class Pet(BaseModel):
    name: str
    health: int = 100
    attack: int = 10


@app.post("/pet/", response_model=dict)
async def create_pet(pet: Pet):
    pet_data = {
        "id": str(uuid.uuid4()),
        "name": pet.name,
        "health": pet.health,
        "attack": pet.attack
    }
    with DaprClient() as dapr:
        dapr.save_state(
            store_name="statestore",
            key=pet_data["id"],
            value=json.dumps(pet_data)
        )
    return pet_data


@app.get("/pet/{pet_id}", response_model=dict)
async def get_pet(pet_id: str):
    with DaprClient() as dapr:
        resp = dapr.get_state(store_name="statestore", key=pet_id)
        pet = json.loads(resp.data.decode("utf-8")) if resp.data else None
        if pet:
            return pet
        return {"error": "Pet not found"}
