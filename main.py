from fastapi import FastAPI, Depends
from database import AsyncSessionLocal
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from models import Event
from sqlalchemy.orm import selectinload
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://csh-50th-website-csh-50th-draft-site.apps.okd4.csh.rit.edu",
        "50th.csh.rit.edu"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/events")
async def events(db = Depends(get_db)):
    result = await db.execute(
        select(Event).options(selectinload(Event.tags))
    )
    event_results = result.scalars().all()

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
            "dress_code": e.dress_code,
            "tags": [t.tag_name for t in e.tags],
        }
        for e in event_results
    ]
