import unittest

from tests.SpiffWorkflow.dmn.DecisionRunner import DecisionRunner


class BoolDecisionTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.7/user-guide/dmn-engine/
    """

    @classmethod
    def setUpClass(cls):
        cls.runner = DecisionRunner('bool_decision.dmn', debug='DEBUG')

    def test_bool_decision_string_output1(self):
        res = self.runner.decide(True)
        self.assertEqual(res.description, 'Y Row Annotation')

    def test_bool_decision_string_output2(self):
        res = self.runner.decide(False)
        self.assertEqual(res.description, 'N Row Annotation')

    def test_bool_decision_string_output3(self):
        res = self.runner.decide(None)
        self.assertEqual(res.description, 'ELSE Row Annotation')

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(BoolDecisionTestClass)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
