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
    table_id = Column(Integer, ForeignKey('tables.id'))
    cells = relationship("Cell", backref="row")

    """
    Args:
        cols: A sequence of values for the columns in this row. Optional.
    """
    def __init__(self, cols=None):
        if cols is None:
            cols = []
        for val in cols:
            cell = Cell(cellContents=val)
            self.cells.append(cell)

class Cell(Base):
    __tablename__ = "cells"
    id  = Column(Integer, primary_key=True)
    cellContents = Column(String)
    row_id = Column(Integer, ForeignKey('rows.id'))