from sqlalchemy import create_engine

# you need to have the Postgres DB up and running: `docker-compose up` ought to do it!
connection_string = "postgresql+psycopg2://usr:pwd@127.0.0.1:5455/demo-db"

# a SQLAlchemy engine implicitly has a connection pool.

# Let's specify some parameters explicitly:
engine = create_engine(
    connection_string,
    echo=True,
    future=True,
    pool_size=3,
    max_overflow=0,
    pool_timeout=2,  # the pool will wait for 2s when you try to open an excess connection
)

# Note that there are different types of pool. The default for postgres is a QueuePool, which behaves as expected.
# However, for SQLite this is a NullPool by default, which actually doesn't pool the connections! That's why we're
# connecting to PostgreSQL for this example.

try:
    print("\n\nOPENING THE MAXIMUM NUMBER OF CONNECTIONS...\n\n")

    c1 = engine.connect()
    c2 = engine.connect()
    c3 = engine.connect()

    print("\n\nNOW OPENING AN EXCESS CONNECTION...\n\n")

    c4 = engine.connect()
except:
    raise
finally:
    # tidy up after ourselves...
    print("\n\nCLOSING ALL THE OPEN CONNECTIONS")
    c1.close(); c2.close(); c3.close()
    closed = [c.closed for c in (c1, c2, c3)]
    print(f"It is {all(closed)} that all connections are now closed")