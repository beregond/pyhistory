import os
import unittest
import shutil

from invoke import run


class TestPyhistory(unittest.TestCase):

    test_dir = 'test_dir'

    def setUp(self):
        try:
            shutil.rmtree(self.test_dir)
        except OSError:
            pass
        os.mkdir(self.test_dir)

        self.original_working_dir = os.getcwd()
        os.chdir(self.test_dir)

    def test_add(self):
        run('pyhi add some_message')

    def tearDown(self):
        os.chdir(self.original_working_dir)
        return
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()
