from sqlalchemy import Column, Integer, Text, Date, Time, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

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

class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String)

    events = relationship("Event", secondary=event_tags, back_populates="tags")