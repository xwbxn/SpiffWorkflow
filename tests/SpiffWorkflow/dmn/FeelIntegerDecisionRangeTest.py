import unittest

from SpiffWorkflow.bpmn.FeelLikeScriptEngine import FeelLikeScriptEngine
from tests.SpiffWorkflow.dmn.DecisionRunner import DecisionRunner


class FeelIntegerDecisionRangeTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.7/user-guide/dmn-engine/
    """
    engine = FeelLikeScriptEngine()

    def test_integer_decision_string_output_inclusive(self):
        runner = DecisionRunner('integer_decision_range_inclusive_feel.dmn',
                                script_engine=self.engine, debug='DEBUG')

        res = runner.decide(100)
        self.assertEqual(res.description, '100-110 Inclusive Annotation')

        res = runner.decide(99)
        self.assertEqual(res.description, 'ELSE Row Annotation')

        res = runner.decide(110)
        self.assertEqual(res.description, '100-110 Inclusive Annotation')

        res = runner.decide(111)
        self.assertEqual(res.description, 'ELSE Row Annotation')

    def test_integer_decision_string_output_exclusive(self):
        runner = DecisionRunner('integer_decision_range_exclusive_feel.dmn',
                                script_engine=self.engine, debug='DEBUG')

        res = runner.decide(100)
        self.assertEqual(res.description, 'ELSE Row Annotation')

        res = runner.decide(101)
        self.assertEqual(res.description, '100-110 Exclusive Annotation')

        res = runner.decide(110)
        self.assertEqual(res.description, 'ELSE Row Annotation')

        res = runner.decide(109)
        self.assertEqual(res.description, '100-110 Exclusive Annotation')

    def test_integer_decision_string_output_excl_inclusive(self):
        runner = DecisionRunner('integer_decision_range_excl_inclusive_feel.dmn',
                                script_engine=self.engine, debug='DEBUG')

        res = runner.decide(100)
        self.assertEqual(res.description, 'ELSE Row Annotation')

        res = runner.decide(101)
        self.assertEqual(res.description, '100-110 ExclInclusive Annotation')

        res = runner.decide(110)
        self.assertEqual(res.description, '100-110 ExclInclusive Annotation')

        res = runner.decide(111)
        self.assertEqual(res.description, 'ELSE Row Annotation')

    def test_integer_decision_string_output_incl_exclusive(self):
        runner = DecisionRunner('integer_decision_range_incl_exclusive_feel.dmn',
                                script_engine=self.engine, debug='DEBUG')

        res = runner.decide(100)
        self.assertEqual(res.description, '100-110 InclExclusive Annotation')

        res = runner.decide(99)
        self.assertEqual(res.description, 'ELSE Row Annotation')

        res = runner.decide(110)
        self.assertEqual(res.description, 'ELSE Row Annotation')

        res = runner.decide(109)
        self.assertEqual(res.description, '100-110 InclExclusive Annotation')

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(FeelIntegerDecisionRangeTestClass)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
