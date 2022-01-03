# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division, absolute_import
from SpiffWorkflow.bpmn.specs.SubWorkflowTask import CallActivity, TransactionSubprocess
from SpiffWorkflow.bpmn.specs.EndEvent import EndEvent
from SpiffWorkflow.bpmn.specs.ExclusiveGateway import ExclusiveGateway
from SpiffWorkflow.bpmn.specs.UserTask import UserTask
from SpiffWorkflow.bpmn.parser.BpmnParser import BpmnParser
from SpiffWorkflow.bpmn.parser.task_parsers import UserTaskParser, EndEventParser, CallActivityParser, TransactionSubprocessParser
from SpiffWorkflow.bpmn.parser.util import full_tag
from SpiffWorkflow.operators import Assign

__author__ = 'matth'

# This provides some extensions to the BPMN parser that make it easier to
# implement testcases


class TestUserTask(UserTask):

    def get_user_choices(self):
        if not self.outputs:
            return []
        assert len(self.outputs) == 1
        next_node = self.outputs[0]
        if isinstance(next_node, ExclusiveGateway):
            return next_node.get_outgoing_sequence_names()
        return self.get_outgoing_sequence_names()

    def do_choice(self, task, choice):
        task.set_data(choice=choice)
        task.complete()

    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_generic(wf_spec, s_state, TestUserTask)


class TestEndEvent(EndEvent):

    def _on_complete_hook(self, my_task):
        my_task.set_data(end_event=self.description)
        super(TestEndEvent, self)._on_complete_hook(my_task)


    def serialize(self, serializer):
        return serializer.serialize_end_event(self)


    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_end_event(wf_spec, s_state, TestEndEvent)


class TestCallActivity(CallActivity):

    def __init__(self, parent, name, **kwargs):
        super(TestCallActivity, self).__init__(parent, name,
                                               out_assign=[Assign('choice', 'end_event')], **kwargs)

    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_subworkflow_task(wf_spec, s_state, TestCallActivity)


class TestTransactionSubprocess(TransactionSubprocess):

    def __init__(self, parent, name, **kwargs):
        super(TestTransactionSubprocess, self).__init__(parent, name,
                                               out_assign=[Assign('choice', 'end_event')], **kwargs)

    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_subworkflow_task(wf_spec, s_state, TestTransactionSubprocess)


class TestBpmnParser(BpmnParser):
    OVERRIDE_PARSER_CLASSES = {
        full_tag('userTask'): (UserTaskParser, TestUserTask),
        full_tag('endEvent'): (EndEventParser, TestEndEvent),
        full_tag('callActivity'): (CallActivityParser, TestCallActivity),
        full_tag('transaction'): (TransactionSubprocessParser, TestTransactionSubprocess),
    }

    def parse_condition(self, condition_expression, outgoing_task, outgoing_task_node, sequence_flow_node, condition_expression_node, task_parser):
        cond = super(
            TestBpmnParser, self).parse_condition(condition_expression, outgoing_task,
                                                  outgoing_task_node, sequence_flow_node, condition_expression_node, task_parser)
        if cond is not None:
            return cond
        return "choice == '%s'" % sequence_flow_node.get('name', None)
