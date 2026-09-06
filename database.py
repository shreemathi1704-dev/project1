from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)


DATABASE_URL = "sqlite:///./agriguard.db"


engine = create_engine(

    DATABASE_URL,

    connect_args={
        "check_same_thread": False
    }

)


SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)


Base = declarative_base()


class Prediction(Base):

    __tablename__ = "predictions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    filename = Column(
        String
    )


    prediction = Column(
        String
    )


    confidence = Column(
        Float
    )


Base.metadata.create_all(
    bind=engine
)