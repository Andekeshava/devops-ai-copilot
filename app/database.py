from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)


DATABASE_URL = "sqlite:///./devops_copilot.db"


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


class AnalysisHistory(Base):

    __tablename__ = "analysis_history"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    issue = Column(
        String,
        nullable=False
    )


    severity = Column(
        String,
        nullable=False,
        default="Medium"
    )


    probable_cause = Column(
        Text,
        nullable=False
    )


    what_to_check = Column(
        Text,
        nullable=False
    )


    commands = Column(
        Text,
        nullable=False
    )


    recommended_fix = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )