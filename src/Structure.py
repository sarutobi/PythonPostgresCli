import datetime
from decimal import Decimal
from operator import contains
from sqlite3 import Timestamp
from typing import List
from typing import Optional

from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    __table_args__ = {"schema": "book"}
    pass

class Bus(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[Optional[String]]
    spec: Mapped[Optional[String]]

class BusRoute(Base):
    __tablename__ = "busroute"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    fkbusstationfrom:Mapped[Optional[int]] = mapped_column(ForeignKey('book.busstation'))
    fkbusstationto:Mapped[Optional[int]] = mapped_column(ForeignKey('book.busstation'))
    distance:Mapped[Optional[int]]
    duration:Mapped[Optional[datetime.datetime]] = mapped_column(Timestamp)

class Busstation(Base):
    __tablename__ = "busstation"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[Optional[String]]
    name: Mapped[Optional[String]]

class Fam(Base):
    __tablename__ = "fam"

    fam: Mapped[Optional[String]]

class Nam(Base):
    __tablename__ = "nam"

    fam: Mapped[Optional[String]]
 
class Ride(Base):
    __tablename__ = "ride"

    id: Mapped[int] = mapped_column(primary_key=True)
    startdate: Mapped[Optional[datetime.date]]
    fkbus: Mapped[Optional[int]] = mapped_column(ForeignKey("book.bus"))
    fkschedule: Mapped[Optional[int]] = mapped_column(ForeignKey("book.schedule"))

class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    fkroute: Mapped[Optional[int]] = mapped_column(ForeignKey("book.busroute"))
    starttime: Mapped[Optional[datetime.time]]
    price: Mapped[Optional[Decimal]]
    validfrom: Mapped[Optional[datetime.date]]
    validto: Mapped[Optional[datetime.date]]

class Seat(Base):
    __tablename__ = "seat"

    id: Mapped[int] = mapped_column(primary_key=True)
    fkbus: Mapped[Optional[int]] = mapped_column(ForeignKey("book.bus"))
    place: Mapped[Optional[VARCHAR]] = mapped_column(String(3))
    fkseatcategory: Mapped[Optional[int]] = mapped_column(ForeignKey("book.seatcategory"))

class Seatcategory(Base):
    __tablename__ = "seatcategory"

    id: Mapped[int] = mapped_column(primary_key=True)
    place: Mapped[String]

class Tickets(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    fkride: Mapped[Optional[int]] = mapped_column(ForeignKey("book.ride"))
    fio: Mapped[String]
    contacts: Mapped[String]
    fkseat: Mapped[Optional[int]] = mapped_column(ForeignKey("book.seat"))