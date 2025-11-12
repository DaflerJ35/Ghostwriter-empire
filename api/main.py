from fastapi import FastAPI, UploadFile
from prisma import Prisma
import nats

app = FastAPI()
db = Prisma()
nc = nats.connect("nats://nats:4222")

@app.post("/ingest/social")
async def ingest_social(data: dict):
    await nc.publish("artist.detected", json.dumps(data).encode())
    return {"status": "emitted"}

@app.post("/tracks/{id}/stems")
async def upload_stems(id: str, file: UploadFile):
    await save_to_s3(file)
    await nc.publish("track.master.requested", json.dumps({"track_id": id}).encode())
    return {"status": "queued"}
