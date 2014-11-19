from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    rows = relationship("Row", backref="table")

    def __repr__(self):
        return "<Table(filename=%s, rawcontents=%s)>" % (self.filename, self.rawcontents)


class Row(Base):
    __tablename__ = "rows"

    id = Column(Integer, primary_key=True)
    rawcontents = Column(String)
    table_id = Column(Integer, ForeignKey('tables.id'))

    def __repr__(self):
        return '<Row %r>' % self.rawcontents