from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///test.db", echo=True, future=True)

print("\n\nCREATING SOME STUFF\n\n")


with engine.connect() as conn:

    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()

print("\n\nFINISHED CREATING SOME STUFF\n\n")


print("\n\nSELECTING SOME STUFF\n\n")

with engine.connect() as conn:

    result = conn.execute(text("SELECT x, y FROM some_table"))

    print("\n\nPRINTING SOME RESULTS\n\n")

    for row in result:
        print(row.x, row.y)

print("\n\nSELECTING AGAIN\n\n")

with engine.connect() as conn:

    result = conn.execute(text("SELECT x, y FROM some_table"))
    
    print("\n\nPRINTING AGAIN\n\n")

    field_names = result.keys()
    data = result.fetchall()

    print(field_names)
    
    for row in data:
        print(row)
