import os
import unittest
import tempfile
import requests

BASE_URL = "http://localhost:5000/"
class ApiTest(unittest.TestCase):

    def test_get_all_files(self):
        r = requests.get('{}/list_files/test_folder'.format(BASE_URL))
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(), [u'file2.txt', u'file3.txt', u'file1.txt', u'.DS_Store', u'file3.jpg', u'file2.jpg', u'file1.jpg'])

    def test_get_files_not_found(self):
        r = requests.get('{}/list_files/Folder'.format(BASE_URL))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'error: Folder does not exits')

    def test_get_txt_files(self):
        r = requests.get('{}/list_files/test_folder/.txt'.format(BASE_URL))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), [u'file2.txt', u'file3.txt', u'file1.txt'])

    def test_get_jpg_files(self):
        r = requests.get('{}/list_files/test_folder/.jpg'.format(BASE_URL))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), [u'file3.jpg', u'file2.jpg', u'file1.jpg'])

    def test_get_jpg_files(self):
        r = requests.get('{}/something'.format(BASE_URL))
        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), u'error: Request is not implemented')

    def test_get_jpg_files(self):
        r = requests.get('{}/blocking'.format(BASE_URL))
        self.assertEqual(r.status_code, 200)

if __name__ == "__main__":
    unittest.main()