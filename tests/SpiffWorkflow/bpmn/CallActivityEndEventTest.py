# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division, absolute_import
import sys
import os
import unittest

from SpiffWorkflow.bpmn.PythonScriptEngine import PythonScriptEngine

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from tests.SpiffWorkflow.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase

__author__ = 'kellym'


class CallActivityTest(BpmnWorkflowTestCase):

    def setUp(self):
        self.spec = self.load_workflow1_spec()

    def load_workflow1_spec(self):
        return self.load_workflow_spec('call_activity_*.bpmn','Process_8200379')

    def testRunThroughHappy(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.workflow.do_engine_steps()

    def testCallActivityHasSameScriptEngine(self):
        self.runCallActivityWithCustomScript()

    def testCallActivityHasSameScriptEngineAfterSaveRestore(self):
        self.runCallActivityWithCustomScript(save_restore=True)

    def runCallActivityWithCustomScript(self, save_restore=False):
        class CustomScriptEngine(PythonScriptEngine):
            pass

        self.workflow = BpmnWorkflow(self.spec,
                                     script_engine=CustomScriptEngine())
        self.workflow.do_engine_steps()
        self.assertTrue(self.workflow.is_completed())
        self.assertIsInstance(self.workflow.script_engine, CustomScriptEngine)

        if save_restore:
            self.save_restore()
            # We have to reset the script engine after deserialize.
            self.workflow.script_engine = CustomScriptEngine()

        # Get the subworkflow
        sub_task = self.workflow.get_tasks_from_spec_name('Sub_Bpmn_Task')[0]
        sub_workflow = sub_task.workflow
        self.assertNotEqual(sub_workflow, self.workflow)
        self.assertIsInstance(self.workflow.script_engine, CustomScriptEngine)
        self.assertEqual(sub_workflow.script_engine, self.workflow.script_engine)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(CallActivityTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
