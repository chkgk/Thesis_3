from otree.api import Currency as c, currency_range
from otree.api import SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants

from random import randint, choice
import itertools


class PlayerBot(Bot):

	def play_round(self):
		# data definition
		test_data = {
			'Comprehension_1': {
				'invalid_inputs': {
					"question_1": ['a', ''], 
					"question_2": ['a', ''], 
					"question_3": ['a', ''], 
					"question_4": ['a', ''], 
					"question_5": ['a', '']
				},
				'valid_inputs': {
					"question_1": True, 
					"question_2": True, 
					"question_3": True, 
					"question_4": True, 
					"question_5": True
				},
			},
			'Comprehension_2': {
				'invalid_inputs': {
					"question_1": ['a', '', True], 
					"question_2": ['a', '', True], 
					"question_3": ['a', '', True], 
					"question_4": ['a', '', True], 
					"question_5": ['a', '', True]
				},
				'valid_inputs': {
					"question_1": True, 
					"question_2": False, 
					"question_3": True, 
					"question_4": False, 
					"question_5": True
				},
			},
			'Questionnaire': {
				'invalid_inputs': {
					'age': [-1, 'a', '', 130],
					'gender': [1, 'cool', ''],
					'studies': 'yay', 
					'nonstudent': 'asd',
					'financial_advice' : ['a', ''], 
					'income': ['a', '']
				},
				'valid_inputs': {
					'age': randint(18, 60),
					'gender': choice(["männlich", "weiblich", "anderes"]),
					'studies': "Economics",
					'nonstudent': False,
					'financial_advice': choice([True, False]), 
					'income': randint(0, 2500)
				}         
			}
		}

		# set whether you want to test all combinations of invalid inputs:
		excessive = False


		# instructions
		# yield (pages.Welcome)
		# yield (pages.Instructions1)
		# yield (pages.Instructions2)

		# Comprehension Questions 1
		# fail
		if excessive:
			keys, values = zip(*test_data['Comprehension_1']['invalid_inputs'].items())
			for v in itertools.product(*values):
				yield SubmissionMustFail(pages.Control_1, dict(zip(keys, v)))

		# pass 
		yield (pages.Control_1, test_data["Comprehension_1"]['valid_inputs'])


		# Comprehension Questions 2
		# fail
		if excessive:
			keys, values = zip(*test_data['Comprehension_2']['invalid_inputs'].items())
			for v in itertools.product(*values):
				yield SubmissionMustFail(pages.Control_2, dict(zip(keys, v)))

		# pass
		yield (pages.Control_2, test_data["Comprehension_2"]['valid_inputs'])


		# category picker
		yield (pages.CategoryPick, {'category': choice(Constants.category_names)})
		
		# agents' decision
		yield (pages.Agent, {'decision_for_principal': 5.0})

		# principal's results
		if self.player.role() == "Principal":
			yield (pages.Results_Principals, {'message': 'Ich bin sehr zufrieden mit Ihrer Entscheidung'})

		# yield (pages.Hilfe4)

		if self.player.role() == "Agent":
			yield (pages.Results_Agents)

		# questionnaire
		# 
		if excessive:
			keys, values = zip(*test_data['Questionnaire']['invalid_inputs'].items())
			for v in itertools.product(*values):
				yield SubmissionMustFail(pages.Questionnaire, dict(zip(keys, v)))

		# manually check field of studies + non student
		yield SubmissionMustFail(pages.Questionnaire, {
					'age': randint(18, 60),
					'gender': choice(["männlich", "weiblich", "anderes"]),
					'studies': "Economics",
					'nonstudent': True,
					'financial_advice': choice([True, False]), 
					'income': randint(0, 2500)
		})

		# manually check no field of studies + indicated that subject is student
		yield SubmissionMustFail(pages.Questionnaire, {
					'age': randint(18, 60),
					'gender': choice(["männlich", "weiblich", "anderes"]),
					'studies': "",
					'nonstudent': False,
					'financial_advice': choice([True, False]), 
					'income': randint(0, 2500)
		})

		# check valid inputs
		yield (pages.Questionnaire, test_data['Questionnaire']['valid_inputs'])

		# last page!
		yield (pages.Last_Page)


# Control_1,
# Control_2,
# CategoryPick,
# CategoryWaitPage,
#     Hilfe,
#     Agent,
#     WaitPage1,
#     Hilfe2,
# #   Hilfe3,
# #   WaitForAgents,
#     Results_Principals,
#     WaitForPrincipals,
#     Hilfe4,
#     Results_Agents,
# #   Questionnaire,
#     Last_Page