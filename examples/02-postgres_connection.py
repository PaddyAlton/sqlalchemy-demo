from sqlalchemy import create_engine, text

# you need to have the Postgres DB up and running: `docker-compose up` ought to do it!
engine = create_engine("postgresql+psycopg2://usr:pwd@127.0.0.1:5455/demo-db", echo=True, future=True)

print("\n\nSELECTING SOME STUFF\n\n")

with engine.connect() as conn:

    result = conn.execute(text("SELECT * FROM attendees"))

    print("\n\nPRINTING SOME RESULTS\n\n")

    for row in result:
        print(row.id, row.name, row.created_at)

    print("\n\nTHOSE WERE THE RESULTS\n\n")
