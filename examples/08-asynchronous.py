import asyncio

from sqlalchemy import Column, DateTime, Integer, String, func, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


Base = declarative_base()
meta = Base.metadata


class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


async def async_main():
    engine = create_async_engine(
        "postgresql+asyncpg://usr:pwd@127.0.0.1:5455/demo-db", echo=True,
    )  # note here the use of asyncpg as the driver library!

    ### COMMENTED OUT, BUT THIS WILL DROP ALL TABLES AND RECREATE FROM MODELS
    # async with engine.begin() as conn:
    #     await conn.run_sync(meta.drop_all)
    #     await conn.run_sync(meta.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit
    # Naturally we also need it to be an AsyncSession, not a regular Session
    MyAsyncSession = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with MyAsyncSession() as session:

        # let's open a transaction
        async with session.begin():
            new_attendee = Attendee(name="A.N. Other")
            session.add(new_attendee)
        # new_attendee auto-committed here

        statement = select(Attendee).order_by(Attendee.created_at.desc())

        results = await session.execute(statement)
    
        for result in results:
            attendee = result[0]
            print(attendee.id, attendee.name, attendee.created_at)

        await session.commit()  # currently working outside a .begin block, so this would be needed to avoid rollback
    
    # session autocloses here

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":

    asyncio.run(async_main())
