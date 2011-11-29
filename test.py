#!/usr/bin/python
import sys, os
import unittest2

SDK_PATH = "/home/ib/Runnables/google_appengine/"
TEST_DIR = os.path.dirname(__file__)

if __name__ == "__main__":
    sys.path.insert(0, SDK_PATH)
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest2.loader.TestLoader().discover(TEST_DIR)
    unittest2.TextTestRunner(verbosity=2).run(suite)    

