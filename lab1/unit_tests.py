import unittest
import pandas as pd
from mathstats import MathStats


class TestMathStats(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_csv('MarketingSpend.csv')
        self.data_marketing = MathStats('MarketingSpend.csv')

    def test_mean(self):
        self.assertAlmostEqual(self.data['Offline Spend'].mean(), self.data_marketing.mean[0])
        self.assertAlmostEqual(self.data['Online Spend'].mean(), self.data_marketing.mean[1])

    def test_max(self):
        self.assertAlmostEqual(self.data['Offline Spend'].max(), self.data_marketing.max[0])
        self.assertAlmostEqual(self.data['Online Spend'].max(), self.data_marketing.max[1])

    def test_min(self):
        self.assertAlmostEqual(self.data['Offline Spend'].min(), self.data_marketing.min[0])
        self.assertAlmostEqual(self.data['Online Spend'].min(), self.data_marketing.min[1])

    def test_disp(self):
        self.assertAlmostEqual(self.data['Offline Spend'].var(), self.data_marketing.disp[0])
        self.assertAlmostEqual(self.data['Online Spend'].var(), self.data_marketing.disp[1])

    def test_sigma_sq(self):
        self.assertAlmostEqual(self.data['Offline Spend'].std(), self.data_marketing.sigma_sq[0])
        self.assertAlmostEqual(self.data['Online Spend'].std(), self.data_marketing.sigma_sq[1])



if __name__ == '__main__':
    unittest.main()
