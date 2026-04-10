from fastapi import FastAPI, Depends, HTTPException
from database import AsyncSessionLocal
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from models import Event, EventTicket
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://csh-50th-website-csh-50th-draft-site.apps.okd4.csh.rit.edu",
        "50th.csh.rit.edu",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={"Access-Control-Allow-Origin": "*"},
    )

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class ScanTicketRequest(BaseModel):
    ticket_id: int
    event_id: int

@app.get("/events")
async def events(db=Depends(get_db)):
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
            "tags": [t.tag_name for t in e.tags]
        }
        for e in event_results
    ]

@app.post("/scan-ticket")
async def scan_ticket(request: ScanTicketRequest, db=Depends(get_db)):
    existing = await db.execute(
        select(EventTicket).where(
            EventTicket.ticket_id == request.ticket_id,
            EventTicket.event_id == request.event_id
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Ticket has already been scanned.")

    new_ticket = EventTicket(
        event_id=request.event_id,
        ticket_id=request.ticket_id,
        used_at=datetime.now(timezone.utc)
    )
    db.add(new_ticket)
    await db.commit()

    return {"success": True, "message": "Ticket scanned successfully."}