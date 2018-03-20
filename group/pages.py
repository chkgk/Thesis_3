from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Control_1(Page):
	
	form_model = "player"
	form_fields = ["question_1", "question_2", "question_3", "question_4", "question_5"]


class Control_2(Page):
	
	form_model = "player"
	form_fields = ["question_1", "question_2", "question_3", "question_4", "question_5"]

	def error_message(self, values):
		if values["question_1"] == 0 or values["question_2"] == 1 or values["question_3"] == 0 or values["question_4"] == 1 or values["question_5"] == 0:
			return "Bitte korrigieren Sie falsch beantwortete Fragen."


class MyPage(Page):
	
	form_model = "player"
	form_fields = ["category"]


class ResultsWaitPage(WaitPage):

	wait_for_all_groups = True
	def after_all_players_arrive(self):
		self.subsession.set_groups()


class Results(Page):
	pass


class Questionnaire(Page):

	form_model = "player"
	form_fields = ["age", "gender", "studies", "studies2", "financial_advice", "income"]

	# returns an error message if a participant...
	def error_message(self, values):
		# ... indicates field of studies and ticks the box "non-student".
		if "studies" in values:
			if values["studies2"] == 1:
				return "You stated a field of studies, but indicated that you are a non-student."
		# ... states no field of studies and and does not tick the box.
		else:
		#elif "studies" not in values:
			if values["studies2"] == 0:
				return "Are you a non-student?"


page_sequence = [
#	Control_1,
#	Control_2,
	MyPage,
	ResultsWaitPage,
	Results,
#	Questionnaire
]
