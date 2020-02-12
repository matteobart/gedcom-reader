import unittest

class TestGedcomMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_example_name(self):
        self.assertTrue(3, 2+1)


#make sure your functions start with the word 'test' and have one 
#parameter self (just because its in a class dw about why)
#ex test_great_name_(self):

if __name__ == '__main__':
    unittest.main()