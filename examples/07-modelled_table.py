from sqlalchemy import Column, DateTime, Integer, String, create_engine, func, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DeclarativeBase = declarative_base()


class Attendee(DeclarativeBase):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=func.now(), nullable=False)


engine = create_engine("postgresql+psycopg2://usr:pwd@127.0.0.1:5455/demo-db", echo=True, future=True)

Session = sessionmaker(engine, future=True)

print("\n\nBEGINNING SESSION\n\n")

with Session.begin() as session:

    print("\n\nCREATING NEW ATTENDEE\n\n")

    new_attendee = Attendee(name="A.N. Other")  # this is 'transient' (not in the DB, not in the session)

    session.add(new_attendee)  # now 'pending' (in the session, not in the DB)

    print("\n\nDONE - AUTO-COMMITTING:\n\n")

    # auto-commits on leaving the context block -> now the new Attendee is in the DB


with Session.begin() as session:

    print("\n\nSELECTING THE NEW ATTENDEE\n\n")

    existing_attendee = session.query(Attendee).filter(Attendee.name=="A.N. Other").first()  # this is 'persistent' (in the DB, in the session)

    print("\n\nDELETING THE NEW ATTENDEE\n\n")

    session.delete(existing_attendee)  # existing_attendee is now in the 'deleted' state - still in the DB though 

    print("\n\nDONE - AUTO-COMMITTING:")

    # auto-commits on leaving the context block -> now existing_attendee is deleted from the DB
    # N.B. the existing_attendee variable is now in the 'detached' state - like 'transient', but known to have been
    # *previously* associated with a DB record

print("\n\nINSPECTING THE existing_attendee VARIABLE...\n")

inspection = inspect(existing_attendee)

print(f"It is {inspection.detached} that existing_attendee is now in the 'detached' state")
