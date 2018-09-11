from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Welcome(Page):
	pass


class Instructions1(Page):
	form_model = "player"
	form_fields = ["question_1", "question_2"]

	def question_1_error_message(self, value):
		if value == "Falsch":
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."

	def question_2_error_message(self, value):
		if value == "Richtig":
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."


class Instructions2(Page):
	form_model = "player"
	form_fields = ["question_3", "question_4"]

	def question_3_error_message(self, value):
		if value != 20:
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."

	def question_4_error_message(self, value):
		if value != 4:
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."


class Instructions3(Page):
	form_model = "player"
	form_fields = ["question_6"]

	def question_6_error_message(self, value):
		if value == "Richtig":
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."



class Agent(Page):
	form_model = "player"
	form_fields = ["decision_for_p1"]


class WaitForAgents(WaitPage):
	def after_all_players_arrive(self):
		self.group.after_investments()


class Results_Principals(Page):	
	def is_displayed(self):
		return self.player.role() == "Principal"


class Results_Agents(Page):
	def is_displayed(self):
		return self.player.role() == "Agent"


class Questionnaire(Page):
	form_model = "player"
	form_fields = ["age", "gender", "studies", "nonstudent", "financial_advice", "income"]

	# This works now, but is not in compliance with the oTree manual.. I guess we found a bug.
	# returns an error message if a participant...
	def error_message(self, values):
		# ... indicates field of studies and ticks the box "non-student".
		if values["studies"]:
			if values["nonstudent"]:
				return "Bitte geben Sie entweder ein Studienfach an oder wählen Sie \"Kein Student\""
		# ... states no field of studies and and does not tick the box.
		else:
		#elif "studies" not in values:
			if not values["nonstudent"]:
				return "Sie haben kein Studienfach angegeben. Wenn Sie kein Student sind, treffen Sie bitte eine entsprechende Auswahl."

	def before_next_page(self):
		self.player.create_gender_dummies()
		self.player.create_econ_dummy()

class Questionnaire2(Page):
	form_model = 'player'
	form_fields = ['em1', 'em2', 'em3', 'em4', 'em5', 'em6', 'em7', 'em8', 'em9', 'em10', 'em11', 'em12', 'em13']

	def before_next_page(self):
		self.player.score_empathy()

class Last_Page(Page):
	pass


page_sequence = [
	Welcome,
	Instructions1,
	Instructions2,
	Instructions3,
	Agent,
	WaitForAgents,
	Results_Principals,
	Results_Agents,
	Questionnaire,
	Questionnaire2,
	Last_Page
]
