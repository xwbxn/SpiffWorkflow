# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division, absolute_import
import sys
import os
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from tests.SpiffWorkflow.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase

__author__ = 'matth'


class MultiInstanceTest(BpmnWorkflowTestCase):
    """The example bpmn diagram has a single task with a loop cardinality of 5.
    It should repeat 5 times before termination."""

    def setUp(self):
        self.spec = self.load_workflow1_spec()

    def load_workflow1_spec(self):
        return self.load_workflow_spec('bpmnMultiUserTask.bpmn','MultiInstance')

    def testRunThroughHappy(self):

        self.workflow = BpmnWorkflow(self.spec)

        for i in range(5):
            self.workflow.do_engine_steps()
            self.assertFalse(self.workflow.is_completed())
            self.do_next_exclusive_step('Activity_Loop')

        self.workflow.do_engine_steps()
        self.assertTrue(self.workflow.is_completed())

    def testSaveRestore(self):

        self.workflow = BpmnWorkflow(self.spec)
        for i in range(5):
            self.save_restore()
            self.workflow.do_engine_steps()
            self.assertFalse(self.workflow.is_completed())
            self.do_next_exclusive_step('Activity_Loop')

        self.workflow.do_engine_steps()
        self.assertTrue(self.workflow.is_completed())

    def testNav(self):
        self.workflow = BpmnWorkflow(self.spec)
        nav = self.workflow.get_flat_nav_list()
        print(nav)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(MultiInstanceTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
