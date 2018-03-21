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

#	def before_next_page(self):
#		self.player.determine_roles()


class ResultsWaitPage(WaitPage):
	
	wait_for_all_groups = True
	def after_all_players_arrive(self):
		self.subsession.set_groups()


class Hilfe(Page):

	##################### Christian: Ich weiß nicht wie ich das ohne eine Hilsseite machen soll ###################################

	def before_next_page(self):
		self.player.determine_roles()
		self.player.get_category()


class Agent(Page):

	form_model = "player"
	form_fields = ["decision_for_principal"]


class WaitPage1(WaitPage):

	def after_all_players_arrive(self):
		self.group.determine_outcome()


class Hilfe2(Page):

	##################### Christian: Ich weiß nicht wie ich das ohne eine Hilsseite machen soll ###################################

	def before_next_page(self):
		self.player.get_investment()
		self.player.calculate_payoffs_principals()


class Results_Principals(Page):
	
	def is_displayed(self):
		return self.player.roles == "Principal"

	form_model = "player"
	form_fields = ["message"]


class WaitForPrincipals(WaitPage):

	def after_all_players_arrive(self):
		pass

class Hilfe4(Page):

	##################### Christian: Ich weiß nicht wie ich das ohne eine Hilsseite machen soll ###################################

	def before_next_page(self):
		self.player.get_message()
		self.player.get_payoff_of_principal()
		self.player.get_profit_of_principal()
		self.player.calculate_payoffs_agents()


class Results_Agents(Page):
	
	def is_displayed(self):
		return self.player.roles == "Agent"


class Questionnaire(Page):

	form_model = "player"
	form_fields = ["age", "gender", "studies", "studies2", "financial_advice", "income"]

	
	####################### Christian: Validating multiple form fields together does not work ######################################
	# returns an error message if a participant...
	def error_message(self, values):
		# ... indicates field of studies and ticks the box "non-student".
		if "studies" in values:
			if values["studies2"]:
				return "You stated a field of studies, but indicated that you are a non-student."
		# ... states no field of studies and and does not tick the box.
		else:
		#elif "studies" not in values:
			if not values["studies2"]:
				return "Are you a non-student?"

class Last_Page(Page):

	pass



page_sequence = [
	Control_1,
	Control_2,
	MyPage,
	ResultsWaitPage,
	Hilfe,
	Agent,
	WaitPage1,
	Hilfe2,
#	Hilfe3,
#	WaitForAgents,
	Results_Principals,
	WaitForPrincipals,
	Hilfe4,
	Results_Agents,
#	Questionnaire,
	Last_Page
]
