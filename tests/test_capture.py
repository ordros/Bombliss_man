import unittest
import capture_bombliss

class CaptureTest(unittest.TestCase):
    def test_fall(self):
            with self.assertRaises(Exception):
                
