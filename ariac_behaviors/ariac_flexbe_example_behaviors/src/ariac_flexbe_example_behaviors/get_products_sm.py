#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.message_state import MessageState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from unit_1_flexbe_behaviors.pick_part_from_bin_sm import pick_part_from_binSM
from unit_1_flexbe_behaviors.place_part_on_agv_sm import place_part_on_agvSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 19 2020
@author: Gerard Harkema
'''
class get_productsSM(Behavior):
	'''
	Getting all the products from a product list.

This example is a part of the order example.
	'''


	def __init__(self):
		super(get_productsSM, self).__init__()
		self.name = 'get_products'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(pick_part_from_binSM, 'pick_part_from_bin')
		self.add_behavior(place_part_on_agvSM, 'place_part_on_agv')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:719 y:341, x:826 y:25
		_state_machine = OperatableStateMachine(outcomes=['finished', 'fail'], input_keys=['Products', 'NumberOfProducts', 'AGVid', 'robot_namespace'])
		_state_machine.userdata.ProductIterator = 0
		_state_machine.userdata.OneValue = 1
		_state_machine.userdata.ProductType = ''
		_state_machine.userdata.ProductPose = []
		_state_machine.userdata.Products = []
		_state_machine.userdata.NumberOfProducts = 0
		_state_machine.userdata.AGVid = ''
		_state_machine.userdata.robot_namespace = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:356 y:121
			OperatableStateMachine.add('GetProduct',
										GetPartFromProductsState(),
										transitions={'continue': 'ProductTypeMessage', 'invalid_index': 'fail'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'Products', 'index': 'ProductIterator', 'type': 'ProductType', 'pose': 'ProductPose'})

			# x:817 y:258
			OperatableStateMachine.add('IncrementProductIterator',
										AddNumericState(),
										transitions={'done': 'CompareProductIterator'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'OneValue', 'result': 'ProductIterator'})

			# x:728 y:120
			OperatableStateMachine.add('ProductPoseMassage',
										MessageState(),
										transitions={'continue': 'pick_part_from_bin'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ProductPose'})

			# x:569 y:121
			OperatableStateMachine.add('ProductTypeMessage',
										MessageState(),
										transitions={'continue': 'ProductPoseMassage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ProductType'})

			# x:1179 y:139
			OperatableStateMachine.add('pick_part_from_bin',
										self.use_behavior(pick_part_from_binSM, 'pick_part_from_bin'),
										transitions={'finished': 'place_part_on_agv', 'failed': 'fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'producttype': 'ProductType', 'robot_namespace': 'robot_namespace', 'robot': 'AGVid'})

			# x:1425 y:142
			OperatableStateMachine.add('place_part_on_agv',
										self.use_behavior(place_part_on_agvSM, 'place_part_on_agv'),
										transitions={'finished': 'IncrementProductIterator', 'failed': 'fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'producttype': 'ProductType', 'AGVid': 'AGVid', 'productpose': 'ProductPose'})

			# x:625 y:256
			OperatableStateMachine.add('CompareProductIterator',
										EqualState(),
										transitions={'true': 'finished', 'false': 'GetProduct'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'NumberOfProducts'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
