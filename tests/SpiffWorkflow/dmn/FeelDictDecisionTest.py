import unittest

from SpiffWorkflow.bpmn.FeelLikeScriptEngine import FeelLikeScriptEngine
from SpiffWorkflow.bpmn.PythonScriptEngine import PythonScriptEngine
from tests.SpiffWorkflow.dmn.DecisionRunner import DecisionRunner


class FeelDictDecisionTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.7/user-guide/dmn-engine/
    """

    @classmethod
    def setUpClass(cls):
        cls.runner = DecisionRunner('dict_decision_feel.dmn',
                                    script_engine=FeelLikeScriptEngine(),
                                    debug='DEBUG')

    def test_string_decision_string_output1(self):
        data = {"allergies": {
                "PEANUTS": {"delicious": True},
                "SPAM": {"delicious": False}
                }}
        PythonScriptEngine.convertToBox(PythonScriptEngine(),data)
        res = self.runner.decide(data)
        self.assertEqual(res.description, 'They are allergic to peanuts')

    def test_string_decision_string_output2(self):
        data = {"allergies": {
                "SpAm": {"delicious": False},
                "SPAM": {"delicious": False}
                }}
        res = self.runner.decide(data)
        self.assertEqual(res.description, 'They are not allergic to peanuts')


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(FeelDictDecisionTestClass)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
