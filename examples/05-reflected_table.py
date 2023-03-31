# reflected_table

from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.orm import Session


engine = create_engine("postgresql+psycopg2://usr:pwd@127.0.0.1:5455/demo-db", echo=True, future=True)


meta = MetaData()

attendees = Table("attendees", meta, autoload_with=engine)


print("\n\nCOMMENCING SELECT IN SESSION\n\n")


with Session(engine, future=True) as session:

    statement = select(attendees).filter_by(name="Paddy")

    result = session.execute(statement)

    print("\n\nRETRIEVED RESULT:\n\n")

    print(result.all())

    print("\n\nENDING SESSION\n\n")
