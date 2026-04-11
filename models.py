from sqlalchemy import Column, Integer, Text, Date, BigInteger, Time, String, Table, ForeignKey, UUID, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()

event_tags = Table(
    "event_tags",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.tag_id"), primary_key=True),
)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    description = Column(Text)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    location_short_name = Column(Text)
    address = Column(Text)
    dress_code = Column(Text)

    tags = relationship("Tag", secondary=event_tags, back_populates="events")
    tickets = relationship("EventTicket", back_populates="event")
    check_ins = relationship("EventNamesList", back_populates="event")

class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String)

    events = relationship("Event", secondary=event_tags, back_populates="tags")

class EventTicket(Base):
    __tablename__ = "event_tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    ticket_id = Column(BigInteger, nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True)

    event = relationship("Event", back_populates="tickets")


class EventNamesList(Base):
    __tablename__ = "event_names_list"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    person_name = Column(Text, nullable=False)
    checked_in = Column(Boolean, nullable=False, default=False)

    event = relationship("Event", back_populates="check_ins")