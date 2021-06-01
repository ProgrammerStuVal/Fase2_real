#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_example_behaviors.get_products_sm import get_productsSM
from ariac_flexbe_states.message_state import MessageState
from ariac_logistics_flexbe_states.get_products_from_shipment_state import GetProductsFromShipmentState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 19 2020
@author: Gerard Harkema
'''
class get_shipmentsSM(Behavior):
	'''
	Tests the starting and stopping of the assignment

This example is a part of the order example.
	'''


	def __init__(self):
		super(get_shipmentsSM, self).__init__()
		self.name = 'get_shipments'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(get_productsSM, 'get_products')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:538 y:468, x:589 y:174
		_state_machine = OperatableStateMachine(outcomes=['finished', 'fail'], input_keys=['Shipments', 'NumberOfShipments'])
		_state_machine.userdata.Shipments = []
		_state_machine.userdata.NumberOfShipments = 0
		_state_machine.userdata.Products = []
		_state_machine.userdata.NumberOfProducts = 0
		_state_machine.userdata.AgvID = ''
		_state_machine.userdata.ShipmentIndex = 1
		_state_machine.userdata.ShipmentType = ''
		_state_machine.userdata.ShipmentIterator = 0
		_state_machine.userdata.OneValue = 1
		_state_machine.userdata.agv1 = 'agv1'
		_state_machine.userdata.arm1 = '/ariac/arm1'
		_state_machine.userdata.arm2 = '/ariac/arm2'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:43 y:24
			OperatableStateMachine.add('GetProducts',
										GetProductsFromShipmentState(),
										transitions={'continue': 'ShipmenTypeMessage', 'invalid_index': 'fail'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'Shipments', 'index': 'ShipmentIterator', 'shipment_type': 'ShipmentType', 'agv_id': 'AgvID', 'products': 'Products', 'number_of_products': 'NumberOfProducts'})

			# x:456 y:344
			OperatableStateMachine.add('CompareShepmentsIterator',
										EqualState(),
										transitions={'true': 'finished', 'false': 'GetProducts'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ShipmentIterator', 'value_b': 'NumberOfShipments'})

			# x:745 y:342
			OperatableStateMachine.add('IncrementShipmentsIterator',
										AddNumericState(),
										transitions={'done': 'CompareShepmentsIterator'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'ShipmentIterator', 'value_b': 'OneValue', 'result': 'ShipmentIterator'})

			# x:252 y:25
			OperatableStateMachine.add('ShipmenTypeMessage',
										MessageState(),
										transitions={'continue': 'AgvIdMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ShipmentType'})

			# x:1008 y:51
			OperatableStateMachine.add('get_products',
										self.use_behavior(get_productsSM, 'get_products'),
										transitions={'finished': 'IncrementShipmentsIterator', 'fail': 'fail'},
										autonomy={'finished': Autonomy.Inherit, 'fail': Autonomy.Inherit},
										remapping={'Products': 'Products', 'NumberOfProducts': 'NumberOfProducts', 'AGVid': 'AgvID', 'robot_namespace': 'robot_namespace'})

			# x:797 y:16
			OperatableStateMachine.add('robot 1 namespace',
										ReplaceState(),
										transitions={'done': 'get_products'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'arm1', 'result': 'robot_namespace'})

			# x:784 y:119
			OperatableStateMachine.add('robot 2 namespace',
										ReplaceState(),
										transitions={'done': 'get_products'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'arm2', 'result': 'robot_namespace'})

			# x:570 y:21
			OperatableStateMachine.add('robot_namespace case',
										EqualState(),
										transitions={'true': 'robot 1 namespace', 'false': 'robot 2 namespace'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'AgvID', 'value_b': 'agv1'})

			# x:416 y:28
			OperatableStateMachine.add('AgvIdMessage',
										MessageState(),
										transitions={'continue': 'robot_namespace case'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'AgvID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
