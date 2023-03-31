# reflected_table

from sqlalchemy import MetaData, create_engine, select
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://usr:pwd@127.0.0.1:5455/demo-db", echo=True, future=True)

meta = MetaData()

meta.reflect(bind=engine)

print(f"\n\n{meta.tables}\n\n")

attendees = meta.tables["attendees"]

print("Here's the attendees table in Python:\n\n", repr(attendees), "\n\n")

MySession = sessionmaker(engine, future=True)

print("\n\nCOMMENCING SELECT IN SESSION\n\n")

with MySession.begin() as session:

    statement = select(attendees).filter_by(name="Paddy")

    result = session.execute(statement)

    print("\n\nRETRIEVED RESULT:\n\n")

    print(result.all())

    print("\n\nENDING SESSION\n\n")  # note that MySession.begin => COMMIT, not ROLLBACK