from sqlalchemy import create_engine, String, Text, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column

DATABASE_URL = "sqlite:///./meetings.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String, index=True)  # removed unique=True
    transcript: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[str] = mapped_column(Text)
    topics: Mapped[str] = mapped_column(Text)


def init_db():
    Base.metadata.create_all(bind=engine)
