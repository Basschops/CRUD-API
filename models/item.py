from datetime import datetime
from sqlalchemy import DateTime, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    file_name = Column(String(240), nullable=False)
    media_type = Column(String(100), nullable=False)
    updated_at = Column(DateTime)
    # lambda function allows freezegun to work in tests
    created_at = Column(DateTime, default=lambda: datetime.now())

    def update(self, file_name=None, media_type=None):
        if file_name is not None:
            self.file_name = file_name
        if media_type is not None:
            self.media_type = media_type
        self.updated_at = datetime.now()
