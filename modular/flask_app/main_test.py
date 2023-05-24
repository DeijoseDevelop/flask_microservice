import unittest

# Discover and load all the tests
test_loader = unittest.TestLoader()
test_suite = test_loader.discover('tests', pattern='test_*.py')

# run the tests
runner = unittest.TextTestRunner()
runner.run(test_suite)
