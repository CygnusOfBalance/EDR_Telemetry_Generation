import telegen
import unittest
import os

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
