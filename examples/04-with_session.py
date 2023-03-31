from sqlalchemy import create_engine, text

from sqlalchemy.orm import Session, sessionmaker


engine = create_engine("sqlite:///:memory:", echo=True, future=True)

print("\n\nCREATING SOME STUFF\n\n")

with Session(engine) as session:

    session.execute(text("CREATE TABLE some_table (x int, y int)"))
    session.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    session.commit()

print("\n\nFINISHED CREATING SOME STUFF\n\n")


print("\n\nSELECTING SOME STUFF\n\n")

# or try this:

MySession = sessionmaker(engine)  # like Engine, MySession is a factory-style object

with MySession() as session:

    result = session.execute(text("SELECT x, y FROM some_table"))

    print("\n\nPRINTING SOME RESULTS\n\n")

    for row in result:
        print(row.x, row.y)
    
    # at this point the session will close

print("\n\nSELECTING AGAIN\n\n")

# N.B. *this version (MySession.begin) autocommits!*
# Here the .begin method starts a new session and a new transaction block
with MySession.begin() as session:

    result = session.execute(text("SELECT x, y FROM some_table"))
    
    print("\n\nPRINTING AGAIN\n\n")

    field_names = result.keys()
    data = result.fetchall()

    print(field_names)
    
    for row in data:
        print(row)

    # At this point the transaction will conclude and be autocommitted
    # and the session will be closed - in SQLAlchemy 2 .begin methods
    # are the way to get autocommitting behaviour.
    # Note that an exception would lead to an autorollback instead!


### FROM THE DOCS - equivalent approaches using sessions vs connections,
### in increasing order of level of transactional control:

# ORM (using 2.0-style Session)                 Core (using 2.0-style engine)
# -----------------------------------------     -----------------------------------
# sessionmaker                                  Engine
# Session                                       Connection
# sessionmaker.begin()                          Engine.begin()
# some_session.commit()                         some_connection.commit()
# with some_sessionmaker() as session:          with some_engine.connect() as conn:
# with some_sessionmaker.begin() as session:    with some_engine.begin() as conn:
# with some_session.begin_nested() as sp:       with some_connection.begin_nested() as sp:
