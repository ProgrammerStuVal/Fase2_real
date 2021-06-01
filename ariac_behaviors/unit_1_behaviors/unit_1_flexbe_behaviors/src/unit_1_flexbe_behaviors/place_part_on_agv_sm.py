#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.add_offset_to_pose_state import AddOffsetToPoseState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_support_flexbe_states.equal_state import EqualState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 31 2021
@author: Nick
'''
class place_part_on_agvSM(Behavior):
	'''
	Behavior for placing objects on agv
	'''


	def __init__(self):
		super(place_part_on_agvSM, self).__init__()
		self.name = 'place_part_on_agv'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		gripper1_service = 'ariac/arm1/gripper/control'
		gripper2_service = 'ariac/arm2/gripper/control'
		# x:653 y:763, x:641 y:356
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['producttype', 'AGVid', 'productpose'])
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.AGVid = ''
		_state_machine.userdata.agv1 = "agv1"
		_state_machine.userdata.robot_config1 = 'R1AGV'
		_state_machine.userdata.robot_config2 = 'R2AGV'
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.frameAGV1 = 'kit_tray_1'
		_state_machine.userdata.frameAGV2 = 'kit_tray_2'
		_state_machine.userdata.robot1_namespace = '/ariac/arm1'
		_state_machine.userdata.robot2_namespace = '/ariac/arm2'
		_state_machine.userdata.AGV_pose = []
		_state_machine.userdata.zero = 0.0
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.gripper1_service = 'ariac/arm1/gripper/control'
		_state_machine.userdata.gripper2_service = 'ariac/arm2/gripper/control'
		_state_machine.userdata.productpose = []
		_state_machine.userdata.producttype = ''
		_state_machine.userdata.part_height_float = 0.1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:549 y:36
			OperatableStateMachine.add('robot case structure',
										EqualState(),
										transitions={'true': 'pre move avg1', 'false': 'pre move avg2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'AGVid', 'value_b': 'agv1'})

			# x:978 y:457
			OperatableStateMachine.add('AGV2 offset',
										AddOffsetToPoseState(),
										transitions={'continue': 'compute placing on AGV2'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'AGV_pose', 'offset_pose': 'productpose', 'output_pose': 'AGV_pose'})

			# x:184 y:639
			OperatableStateMachine.add('actual placing on top of AGV1',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'de-attach object from gripper', 'planning_failed': 'retry move to AGV1', 'control_failed': 'retry move to AGV1'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot1_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:973 y:630
			OperatableStateMachine.add('actual placing on top of AGV2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'de-attach object from gripper_2', 'planning_failed': 'retry move to AGV2', 'control_failed': 'retry move to AGV2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot2_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:187 y:546
			OperatableStateMachine.add('compute placing on AGV1',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'actual placing on top of AGV1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'robot1_namespace', 'tool_link': 'tool_link', 'pose': 'AGV_pose', 'offset': 'part_height_float', 'rotation': 'zero', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:977 y:539
			OperatableStateMachine.add('compute placing on AGV2',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'actual placing on top of AGV2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'robot2_namespace', 'tool_link': 'tool_link', 'pose': 'AGV_pose', 'offset': 'part_height_float', 'rotation': 'zero', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:185 y:734
			OperatableStateMachine.add('de-attach object from gripper',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'wait for part to get dropped', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper1_service'})

			# x:975 y:725
			OperatableStateMachine.add('de-attach object from gripper_2',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'wait for part to get dropped_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper2_service'})

			# x:190 y:362
			OperatableStateMachine.add('get location agv1',
										GetObjectPoseState(),
										transitions={'continue': 'AGV1 offset', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'frame': 'frameAGV1', 'pose': 'AGV_pose'})

			# x:978 y:364
			OperatableStateMachine.add('get location agv2',
										GetObjectPoseState(),
										transitions={'continue': 'AGV2 offset', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'frame': 'frameAGV2', 'pose': 'AGV_pose'})

			# x:190 y:248
			OperatableStateMachine.add('move to agv1',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'get location agv1', 'planning_failed': 'retry premove agv1', 'control_failed': 'retry premove agv1'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot1_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:184 y:1047
			OperatableStateMachine.add('move to agv1_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'finished', 'planning_failed': 'retry premove agv1_2', 'control_failed': 'retry premove agv1_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot1_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:981 y:1031
			OperatableStateMachine.add('move to agv1_2_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'finished', 'planning_failed': 'retry premove agv1_2_2', 'control_failed': 'retry premove agv1_2_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot2_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:975 y:261
			OperatableStateMachine.add('move to agv2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'get location agv2', 'planning_failed': 'retry premove agv2', 'control_failed': 'retry premove agv2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'robot2_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:193 y:136
			OperatableStateMachine.add('pre move avg1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move to agv1', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config1', 'move_group': 'move_group', 'action_topic_namespace': 'robot1_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:185 y:907
			OperatableStateMachine.add('pre move avg1_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move to agv1_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config1', 'move_group': 'move_group', 'action_topic_namespace': 'robot1_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:978 y:906
			OperatableStateMachine.add('pre move avg1_2_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move to agv1_2_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config2', 'move_group': 'move_group', 'action_topic_namespace': 'robot2_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:970 y:144
			OperatableStateMachine.add('pre move avg2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move to agv2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config2', 'move_group': 'move_group', 'action_topic_namespace': 'robot2_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:19 y:640
			OperatableStateMachine.add('retry move to AGV1',
										WaitState(wait_time=1),
										transitions={'done': 'actual placing on top of AGV1'},
										autonomy={'done': Autonomy.Off})

			# x:1218 y:630
			OperatableStateMachine.add('retry move to AGV2',
										WaitState(wait_time=1),
										transitions={'done': 'actual placing on top of AGV2'},
										autonomy={'done': Autonomy.Off})

			# x:32 y:250
			OperatableStateMachine.add('retry premove agv1',
										WaitState(wait_time=1),
										transitions={'done': 'move to agv1'},
										autonomy={'done': Autonomy.Off})

			# x:9 y:1049
			OperatableStateMachine.add('retry premove agv1_2',
										WaitState(wait_time=1),
										transitions={'done': 'move to agv1_2'},
										autonomy={'done': Autonomy.Off})

			# x:1235 y:1033
			OperatableStateMachine.add('retry premove agv1_2_2',
										WaitState(wait_time=1),
										transitions={'done': 'move to agv1_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:1217 y:264
			OperatableStateMachine.add('retry premove agv2',
										WaitState(wait_time=1),
										transitions={'done': 'move to agv2'},
										autonomy={'done': Autonomy.Off})

			# x:183 y:820
			OperatableStateMachine.add('wait for part to get dropped',
										WaitState(wait_time=1),
										transitions={'done': 'pre move avg1_2'},
										autonomy={'done': Autonomy.Off})

			# x:977 y:829
			OperatableStateMachine.add('wait for part to get dropped_2',
										WaitState(wait_time=1),
										transitions={'done': 'pre move avg1_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:190 y:457
			OperatableStateMachine.add('AGV1 offset',
										AddOffsetToPoseState(),
										transitions={'continue': 'compute placing on AGV1'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'AGV_pose', 'offset_pose': 'productpose', 'output_pose': 'AGV_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
