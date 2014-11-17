from sqlalchemy import Column, Integer, String
from database import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    rawcontents = Column(String)

    def __repr__(self):
        return "<Table(filename=%s, rawcontents=%s)>" % (self.filename, self.rawcontents)
