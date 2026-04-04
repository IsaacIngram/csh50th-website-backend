from sqlalchemy import Column, Integer, Text, Date, Time
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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