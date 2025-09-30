from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DatabaseAsyncSession:
    def __init__(self, db_url: str, echo: bool = False):
        self.engine = create_async_engine(db_url, echo=echo)
        self.SessionLocal = async_sessionmaker(bind=self.engine, expire_on_commit=False)

