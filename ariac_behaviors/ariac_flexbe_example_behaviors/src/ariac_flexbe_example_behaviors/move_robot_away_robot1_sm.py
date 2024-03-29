#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 31 2021
@author: Nick
'''
class Move_robot_away_robot1SM(Behavior):
	'''
	Behavior to move robot 1 or 2 out of eachothers ways
	'''


	def __init__(self):
		super(Move_robot_away_robot1SM, self).__init__()
		self.name = 'Move_robot_away_robot1'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:858 y:94, x:481 y:329
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.robot_namespace = '/ariac/arm1'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.home = 'R1bin6PreGrasp'
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.pre_home = 'R1bin5PreGrasp'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:75 y:99
			OperatableStateMachine.add('movePre prehome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveTo bin 5', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'pre_home', 'move_group': 'move_group', 'action_topic_namespace': 'robot_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:589 y:97
			OperatableStateMachine.add('MoveTo home',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'finished', 'planning_failed': 'retry move away', 'control_failed': 'retry move away'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:415 y:98
			OperatableStateMachine.add('movePre home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveTo home', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home', 'move_group': 'move_group', 'action_topic_namespace': 'robot_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:620 y:192
			OperatableStateMachine.add('retry move away',
										WaitState(wait_time=1),
										transitions={'done': 'movePre prehome'},
										autonomy={'done': Autonomy.Off})

			# x:239 y:98
			OperatableStateMachine.add('MoveTo bin 5',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'movePre home', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
