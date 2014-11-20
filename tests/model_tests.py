import unittest
from models import *

class TestModels(unittest.TestCase):

    def test_cell(self):
        cell = Cell(cell_contents="whisky")

    def test_row(self):
        cols =["one bourbon", "one scotch", "one beer"]
        row = Row()
        row.populate(cols)
        self.assertTrue(len(row.cells) == 3)
        self.assertEqual(row.cells[0].cell_contents, "one bourbon")
        self.assertEqual(row.cells[1].cell_contents, "one scotch")
        self.assertEqual(row.cells[2].cell_contents, "one beer")

    def test_table(self):
        file_name = "the_file_name.csv"
        table = Table(file_name)

        file_contents = """ headerA,headerB,headerC,headerD
                        aaa,bbb,cc,ddddd
                        1,2,44,10"""
        for line in file_contents.split('\n'):
            cols = line.split(',')
            r = Row().populate(cols)
            print(type(r))
            table.rows.append(cols)

        self.assertEqual(len(table.rows),3)

if __name__ == '__main__':
    unittest.main()
