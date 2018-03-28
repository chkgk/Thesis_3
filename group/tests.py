from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

	def play_round(self):
		yield (pages.Welcome)
		yield (pages.Instructions1)
		yield (pages.CategoryElicitation, {'cat_end_rel_1', 'cat_end_rel_2', 'cat_end_rel_3', 'cat_end_rel_4', 'cat_end_rel_5',	'cat_end_abs_1', 'cat_end_abs_2', 'cat_end_abs_3', 'cat_end_abs_4', 'cat_end_abs_5',})
		yield (pages.Instructions2)
		yield (pages.Control_1, {"question_1": "Falsch", "question_2": "Richtig", "question_3": "Falsch", "question_4": 10, "question_5": 6})
		yield (pages.Control_2, {"question_1": "Falsch", "question_2": "Richtig", "question_3": "Falsch", "question_4": 10, "question_5": 6})
		yield (pages.CategoryPick, {"category": "Sicherheitsorientiert"})
		yield (pages.Agent, {"decision_for_p1": 5})
		yield (pages.Results_Principal, {"message": "Ich bin sehr zufrieden"})
		yield (pages.Results_Agent)
		yield (pages.Questionnaire, {"age": 12, "gender": "female", "studies": "English", "nonstudent": "Kein Student", "financial_advice": "Ja", "income": 12})
		yield (pages.Last_Page)

