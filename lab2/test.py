import unittest
import utils


class TestMemoized(unittest.TestCase):
    def test_memoized(self):
        utils.factorial_cashe(32)
        utils.factorial_cashe(35)
        utils.factorial_cashe(37)

        utils.factorial_cashe_copy(25)

        cache1 = utils.get_cache(utils.factorial_cashe)
        cache2 = utils.get_cache(utils.factorial_cashe_copy)

        self.assertNotEqual(cache1, cache2)

        utils.save_cache(cache1, 'cache1.json')
        utils.load_cache('cache1.json', utils.factorial_cashe_copy)
        cache2 = utils.get_cache(utils.factorial_cashe_copy)

        self.assertEqual(cache1, cache2)
