import telegen
import unittest
import os

#-------------------------------------------------------------------------------
# This file is not meant to be for comprehensive unit testing. For the sake of
# time, I threw together some basic basecase unit tests in order to show I am
# capable of writing them and am aware of the importance and power of them.
#-------------------------------------------------------------------------------
class TestFileMethods(unittest.TestCase):
    def test_create_base(self):
        telegen.createFile("./test.py")
        self.assertTrue(os.path.exists("./test.py"))
        os.remove("./test.py")

    def test_modify_base(self):
        f=open("./test.py", "w+")
        f.close()
        telegen.modifyFile("./test.py")
        with open("./test.py") as a:
            self.assertTrue('THIS IS A FILE MODIFICATION' in a.read())

        a.close()
        os.remove("./test.py")

    def test_delete_base(self):
        f=open("./test.py", "a+")
        f.close()
        telegen.deleteFile("./test.py")
        self.assertFalse(os.path.exists("./test.py"))

if __name__ == "__main__":
    unittest.main(buffer=True, exit=False)
