from mongoengine import Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField

# TODO how can I define a custom __init__ method for these? My attempts yield 'object has no attribute _data'

class Cell(EmbeddedDocument):
    cell_contents = StringField(max_length=1000)


class Row(EmbeddedDocument):
    cells = ListField(EmbeddedDocumentField(Cell))

    def populate(self, cols):
        for val in cols:
            c = Cell(cell_contents=val)
            self.cells.append(c)

class Table(Document):
    '''
    A user-supplied source of tabular data
    '''
    file_name = StringField(required=True)
    rows = ListField(EmbeddedDocumentField(Row))

    # TODO: methods to populate table by parsing input files

