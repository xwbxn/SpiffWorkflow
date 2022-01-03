# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division, absolute_import
import unittest
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from tests.SpiffWorkflow.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase

__author__ = 'leashys'


class ParallelWithScriptTest(BpmnWorkflowTestCase):

    def setUp(self):
        self.spec = self.load_workflow1_spec()

    def load_workflow1_spec(self):
        return self.load_workflow_spec('ParallelWithScript.bpmn','ParallelWithScript')

    def testRunThroughParallel(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.workflow.do_engine_steps()
        nav_list = self.workflow.get_flat_nav_list()
        for nav in nav_list:
            print(nav)
        self.assertNav(nav_list[0], name="StartEvent_1", indent=0)
        self.assertNav(nav_list[1], name="Gateway_1", indent=0)
        self.assertNav(nav_list[2], description="Task A", indent=1)
        self.assertNav(nav_list[3], description="Task B", indent=1)
        self.assertNav(nav_list[4], description="Script", indent=1)
        self.assertNav(nav_list[5], description="Task C", indent=1)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ParallelWithScriptTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
