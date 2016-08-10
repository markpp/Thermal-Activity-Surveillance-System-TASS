"""
This file contain a few simple unittests

"""
import unittest
import numpy as np
import sys
sys.path.append('../')
import tools


"""My unittesting class.

"""
class unitTests(unittest.TestCase):


    # def testFail(self):
    """Simple test that should always fail.
    """
    #    self.failUnless(False)


    def test_pass(self):
        """Simple test that should always pass.
        """
        self.failUnless(True)


    def test_configuration(self):
        """Test that the loaded configuration is acceptable.

        It is tested that loading the configuration file is working and that the specified
        sample and step size is acceptable.
        """
        json = tools.filehandler.load_config()
        # Unless result data type is changed, max_iter must be less than or equal to 256 and greater than 0
        self.assertLessEqual(json["general"]["max_iter"], 256)
        self.assertGreater(json["general"]["max_iter"], 0)
        # The number of workers should be greater than or equal to 1
        self.assertGreaterEqual(json["general"]["num_workers"], 1)


    def test_results(self):
        """Test that the results of each implementation are the same.

        It is verified whether the result matrices are identical across implementations.
        """
        # Load the result matrix for the naive approach
        baseline_result = tools.filehandler.unpickle_result("../output/naive/res_data.pickle")
        # Compare shape and each element between results of each of the approaches
        np.testing.assert_array_equal(baseline_result,
                                      tools.filehandler.unpickle_result("../output/parallel/res_data.pickle"))
        np.testing.assert_array_equal(baseline_result,
                                      tools.filehandler.unpickle_result("../output/compiled/res_data.pickle"))


if __name__ == '__main__':
    """Main function for running the unit test script.

    """
    unittest.main()
