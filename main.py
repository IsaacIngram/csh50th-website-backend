from fastapi import FastAPI, Depends
from database import AsyncSessionLocal

from sqlalchemy.future import select
from models import Event
app = FastAPI()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/events")
async def events(db = Depends(get_db)):
    result = await db.execute(select(Event))
    event_results = result.scalars.all()

    return [
        {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "date": e.date,
            "start_time": e.start_time,
            "end_time": e.end_time,
            "location_short_name": e.location_short_name,
            "address": e.address,
            "dress_code": e.dress_code
        }
        for e in event_results
    ]
