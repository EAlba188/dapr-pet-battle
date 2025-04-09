from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dapr.clients.grpc.client import DaprGrpcClient as DaprClient
import random
import json

app = FastAPI()


class BattleRequest(BaseModel):
    pet1_id: str
    pet2_id: str


@app.post("/battle/", response_model=dict)
async def start_battle(battle: BattleRequest):
    with DaprClient() as dapr:
        # Obtener pet1
        pet1_resp = dapr.invoke_method(
            app_id="petservice",
            method_name=f"pet/{battle.pet1_id}",
            data=b"",
            http_verb="GET"
        )
        pet1 = json.loads(pet1_resp.data.decode("utf-8")) if pet1_resp.data else None

        # Obtener pet2
        pet2_resp = dapr.invoke_method(
            app_id="petservice",
            method_name=f"pet/{battle.pet2_id}",
            data=b"",
            http_verb="GET"
        )
        pet2 = json.loads(pet2_resp.data.decode("utf-8")) if pet2_resp.data else None

        if not pet1 or not pet2:
            raise HTTPException(status_code=404, detail="One or both pets not found")

        winner = pet1["name"] if random.randint(0, 1) == 0 else pet2["name"]
        result = {
            "winner": winner,
            "pet1": pet1["name"],
            "pet2": pet2["name"]
        }

        dapr.publish_event(
            pubsub_name="pubsub",
            topic_name="battle-results",
            data=json.dumps(result)
        )

    return result
