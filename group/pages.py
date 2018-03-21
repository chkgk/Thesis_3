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


class Hilfe(Page):

	##################### Christian: Ich weiß nicht wie ich das ohne eine Hilsseite machen soll ###################################

	def before_next_page(self):
		self.player.determine_roles()
		self.player.find_principals()
		self.player.find_partners()
		self.player.get_category()


class Agent(Page):

	def vars_for_template(self):
		group = self.group.get_players()

		return {'p1_category': group[int(self.player.c_principal_1)-1].category , 'p2_category': group[int(self.player.c_principal_2)-1].category, 'p3_category': group[int(self.player.c_principal_3)-1].category, 'p4_category': group[int(self.player.c_principal_4)-1].category, 'p5_category': group[int(self.player.c_principal_5)-1].category}
	

	form_model = "player"
	form_fields = ["decision_for_p1", "decision_for_p2", "decision_for_p3", "decision_for_p4","decision_for_p5"]

	def before_next_page(self):
		self.player.determine_outcome()

class WaitPage1(WaitPage):

	def after_all_players_arrive(self):
		pass

class Hilfe2(Page):

	##################### Christian: Ich weiß nicht wie ich das ohne eine Hilsseite machen soll ###################################

	def before_next_page(self):
		self.player.get_investment()
		self.player.calculate_payoffs_principals()
		self.player.get_outcome_of_principal()


class Results_Principal(Page):

	def is_displayed(self):
		return self.player.roles == "Principal"

	form_model = "player"
	form_fields = ["message"]


class WaitPage2(WaitPage):

	def after_all_players_arrive(self):
		pass


class Hilfe3(Page):

	def before_next_page(self):
		self.player.get_invested_amount()
		self.player.get_message()
		self.player.get_payoff_of_principal()
		self.player.get_profit_of_principal()
		self.player.calculate_payoffs_agents()


class Results_Agent(Page):

	def is_displayed(self):
		return self.player.roles == "Agent"


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


class Last_Page(Page):

	pass


page_sequence = [
#	Control_1,
#	Control_2,
	MyPage,
	ResultsWaitPage,
	Hilfe,
	Agent,
	WaitPage1,
	Hilfe2,
	Results_Principal,
	WaitPage2,
	Hilfe3,
	Results_Agent,
#	Questionnaire,
	Last_Page
]
