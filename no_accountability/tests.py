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
                    "question_1": ['a', 5],
                    "question_2": ['a', ''],
                    "question_3": ['a', ''],
                    "question_4": ['a', ''],
                    "question_5": ['a', '']
                },
                'valid_inputs': {
                    "question_1": "Falsch",
                    "question_2": "Richtig",
                    "question_3": "Falsch",
                    "question_4": 10,
                    "question_6": "Falsch"
                },
            },
            'Comprehension_2': {
                'invalid_inputs': {
                    "question_1": ['a', '', True],
                    "question_2": ['a', '', True],
                    "question_3": ['a', '', True],
                    "question_4": ['a', '', True],
                    "question_6": ['a', '', True]
                },
                'valid_inputs': {
                    "question_1": "Falsch",
                    "question_2": "Richtig",
                    "question_3": "Falsch",
                    "question_4": 10,
                    "question_6": "Falsch"
                },
            },
            'Questionnaire': {
                'invalid_inputs': {
                    'age': [-1, 'a', '', 130],
                    'gender': [1, 'cool', ''],
                    'studies': 'yay',
                    'nonstudent': 'asd',
                    'financial_advice': ['a', ''],
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
            },
            'Questionnaire_2': {
                'invalid_inputs': {
                    'em1': -1,
                    'em2': -1,
                    'em3': -1,
                    'em4': -1,
                    'em5': -1,
                    'em6': -1,
                    'em7': -1,
                    'em8': 5,
                    'em9': 5,
                    'em10': 5,
                    'em11': 5,
                    'em12': 5,
                    'em13': 5,
                },
                'valid_inputs': { # em score 9 after transformation
                    'em1': 1,
                    'em2': 2,
                    'em3': 3,
                    'em4': 4,
                    'em5': 1,
                    'em6': 2,
                    'em7': 3,
                    'em8': 4,
                    'em9': 1,
                    'em10': 2,
                    'em11': 3,
                    'em12': 4,
                    'em13': 1,
                }
            }
        }

        # set whether you want to test all combinations of invalid inputs:
        excessive = False

        # welcome
        yield (pages.Welcome)

        # instructions 1
        yield SubmissionMustFail(pages.Instructions1, {'question_1': 'Falsch', 'question_2': 'Falsch'})
        yield SubmissionMustFail(pages.Instructions1, {'question_1': 'Falsch', 'question_2': 'Richtig'})
        yield (pages.Instructions1, {'question_1': 'Richtig', 'question_2': 'Falsch'})

        # instructions 2
        yield SubmissionMustFail(pages.Instructions2, {'question_3': randint(21, 2500), 'question_4': randint(0, 3)})
        yield (pages.Instructions2, {'question_3': 20, 'question_4': 4})

        # instructions 3
        yield SubmissionMustFail(pages.Instructions3, {'question_6': 'Richtig'})
        yield (pages.Instructions3, {'question_6': 'Falsch'})

        # agents' decision
        yield (pages.Agent, {'decision_for_p1': 7.5})

        # principal's results
        if self.player.role() == "Principal":
            assert self.player.investment == 7.5
            if self.group.investment_success == 0:
                assert self.player.payoff == 2.5
            else:
                assert self.player.payoff == 28.75
            yield (pages.Results_Principals)

        # agents' results
        if self.player.role() == "Agent":
            if self.group.investment_success == 0:
                assert self.player.payoff_of_principal == 2.5
                assert self.player.profit_of_principal == 0
                if self.player.compensation == "variable_result":
                    assert self.player.payoff == 5.625
                else:
                    assert self.player.payoff == Constants.fixed_payment
            else:
                assert self.player.payoff_of_principal == 28.75
                assert self.player.profit_of_principal == 18.75
                if self.player.compensation == "fixed":
                    assert self.player.payoff == Constants.fixed_payment
                elif self.player.compensation == "variable_result":
                    assert self.player.payoff == 12.1875
                elif self.player.compensation == "variable_profit":
                    assert self.player.payoff == 11.5625
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


        # EQ 13 questionnaire
        yield SubmissionMustFail(pages.Questionnaire2, test_data["Questionnaire_2"]['invalid_inputs'])
        yield (pages.Questionnaire2, test_data['Questionnaire_2']['valid_inputs'])
        assert self.player.em_score == 9

        # last page!
        if self.player.role() == "Agent":
            if self.group.investment_success == 0:
                if self.player.compensation == "variable_result":
                    assert self.player.payoff + self.player.participation_fee == 9.625
                else:
                    assert self.player.payoff + self.player.participation_fee == 9
        if self.player.role() == "Principal":
            if self.group.investment_success == 0:
                assert self.player.payoff + self.player.participation_fee == 6.5
            else:
                assert self.player.payoff + self.player.participation_fee == 32.75

# Welcome,
# Instructions1,
# Instructions2,
# Instructions3,
# Agent,
# WaitForAgents,
# Results_Principals,
# Results_Agents,
# Questionnaire,
# Questionnaire_2,
# Last_Page
