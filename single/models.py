from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'single'
	players_per_group = None
	num_rounds = 1

	category_names = ['Sehr Konservativ', 'Sicherheitsorientiert', 'Ausgeglichen', 'Wachstumsorientiert', 'Offensiv']

	endowment_principals = c(10)

	# Fixed Compensation
	fixed_payment = c(10)

	#Variable Compensation
	variable_payment = c(5)			# Fixer Anteil für die Agenten
	share_result = 25				# In Prozent
	share_profit = 25

class Subsession(BaseSubsession):

	def creating_session(self):
		random_number = random.randint(1,2)
		player_list = self.get_players()
		for player in player_list:
			player.compensation = self.session.config["compensation"]
			player.participation_fee = self.session.config["participation_fee"]
			player.random_number = random_number
	
	def set_groups(self):

		# Create category lists

		cat_lists = dict.fromkeys(Constants.category_names)
		for element in cat_lists:
			cat_lists[element] = []

		# sort players into category lists by their choices
		for player in self.get_players():
			for cat_name in cat_lists:
				if player.category == cat_name:
					cat_lists[cat_name].append(player)
					

		total_players = len(self.get_players())
		group_size = 2
		number_groups = int(total_players / group_size)

		print(cat_lists)

		groups = [[] for i in range(number_groups)]
		temp = []
		for i in range(len(Constants.category_names)):
			for j in range(len(cat_lists[Constants.category_names[i]])):
				temp.append(cat_lists[Constants.category_names[i]][j])
		
		print(temp)
		for i in range(number_groups):
			print(temp[i::number_groups])
			groups[i].append(temp[i::number_groups])

		print([l[0] for l in groups])		# macht ne Klammer weniger
		matrix = [l[0] for l in groups]

		# matrix = [[2, 1], [4,3]]


		self.set_group_matrix(matrix)

		print(self.get_group_matrix())

		group_matrix = self.get_group_matrix()
		for group in group_matrix:
			for player in group:
				player.my_group_id = group_matrix.index(group) + 1



class Group(BaseGroup):
	
	def determine_outcome(self):
		randomizer = random.randint(1,3)
		if randomizer == 1:
			self.investment_outcome = 1
		else:
			self.investment_outcome = 0

	investment_outcome = models.IntegerField(
		doc="Turns 1 if the investment was successful and 0 in case it was not."
		)


class Player(BasePlayer):
	
	my_group_id = models.IntegerField()

	random_number = models.IntegerField()

	compensation = models.CharField(
		doc="Compensation scheme put in place for agents (see Settings)."
		)

	participation_fee = models.CurrencyField(
		doc="Participation fee for all agents."
		)



	roles = models.CharField()
	# Mit der normalen role Funktion klappt es nicht, dass ich die Results Seiten auf die Rolle bedinge.

	def determine_roles(self):
		if self.id_in_group == self.random_number:
			self.roles = "Principal"
		else:
			self.roles = "Agent"


# Everyone chooses the category:

	category = models.CharField(
		choices=Constants.category_names,
		widget=widgets.RadioSelect(),
		verbose_name="Bitte wählen Sie nun einen der fünf Begriffe:",
		doc="Principals choose the category which is communicated to their agent"
		)


	category_from_principal = models.CharField(
		doc="Category that agents receive from their principals indicating how they want their agent to invest."
		)


	def get_category(self):
		principal = self.get_others_in_group()[0]
		self.category_from_principal = principal.category


# Everyone takes the investment decision for their principal:

	decision_for_principal = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	investment = models.CurrencyField(
		doc="Indicates for everyone the investment decision as taken by their agents."
		)

	def get_investment(self):
		agent = self.get_others_in_group()[0]
		self.investment = agent.decision_for_principal


# principals can send messages to their agents:

	message = models.CharField(
		choices=["Ich bin sehr zufrieden mit Ihrer Entscheidung", "Ich bin zufrieden mit Ihrer Entscheidung",
		"Ich bin unzufrieden mit Ihrer Entscheidung", "Ich bin sehr unzufrieden mit Ihrer Entscheidung"],
		widget=widgets.RadioSelect(),
		verbose_name="Wählen Sie dazu eine der vorgefertigten Mitteilungen aus:",
		doc="Principals choose the message to send to the agents."
		)

	message_from_principal = models.CharField(
		doc="Message that agents receive from their principals."
		)

	def get_message(self):
		principal = self.get_others_in_group()[0]
		self.message_from_principal = principal.message




# Payoffs:

	def calculate_payoffs_principals(self):
		if self.roles == "Principal":
			if self.group.investment_outcome == 1:
				self.payoff = self.investment * 3.5 + (Constants.endowment_principals - self.investment)
				self.profit = self.investment * 2.5
			elif self.group.investment_outcome == 0:
				self.payoff = Constants.endowment_principals - self.investment
				self.profit = 0

	profit = models.CurrencyField(
		doc="Gives the profit of the principal."
		)

	payoff_of_principal = models.CurrencyField(
		doc="Gives for each agent the payoff of his principal."
		)

	def get_payoff_of_principal(self):
		principal = self.get_others_in_group()[0]
		self.payoff_of_principal = principal.payoff



	profit_of_principal = models.CurrencyField(
		doc="Gives for each agent the payoff of his principal."
		)

	def get_profit_of_principal(self):
		principal = self.get_others_in_group()[0]
		self.profit_of_principal = principal.profit


	def calculate_payoffs_agents(self):
		if self.roles == "Agent":
			if self.compensation == "fixed":
				self.payoff = Constants.fixed_payment
			if self.compensation == "variable_result":
				self.payoff = Constants.variable_payment + Constants.share_result/100 * self.payoff_of_principal
			if self.compensation == "variable_profit":
				self.payoff = Constants.variable_payment + Constants.share_profit/100 * self.profit_of_principal





	# Control Questions

	question_1 = models.BooleanField(
		verbose_name="Blabla1",
		widget=widgets.RadioSelect(),
		)

	question_2 = models.BooleanField(
		verbose_name="Blabla2",
		widget=widgets.RadioSelect(),
		)

	question_3 = models.BooleanField(
		verbose_name="Blabla3",
		widget=widgets.RadioSelect(),
		)

	question_4 = models.BooleanField(
		verbose_name="Blabla4",
		widget=widgets.RadioSelect(),
		)

	question_5 = models.BooleanField(
		verbose_name="Blabla5",
		widget=widgets.RadioSelect(),
		)



	# Questionnaire:

	age = models.PositiveIntegerField(
		max=100,
		verbose_name="Wie alt sind Sie?",
		doc="We ask participants for their age between 0 and 100 years"
		)

	gender = models.CharField(
		choices=["männlich", "weiblich", "anderes"],
		widget=widgets.RadioSelect(),
		verbose_name="Was ist Ihr Geschlecht?",
		doc="gender indication"
		)

	studies = models.CharField(
		blank=True,
		verbose_name="Was studieren Sie im Hauptfach?",
		doc="field of studies indication."
		)

	studies2 = models.BooleanField(
		widget=widgets.CheckboxInput(),
		verbose_name="Kein Student",
		doc="Ticking the checkbox means that the participant is a non-student.")

	financial_advice = models.CharField(
		choices=["Ja", "Nein"],
		widget=widgets.RadioSelect(),
		verbose_name="Haben Sie bereits eine Bankberatung in Anspruch genommen?",
		doc="We ask participants if they ever made use of financial advice.")

	income = models.CurrencyField(
		verbose_name="Wie viel Geld im Monat steht Ihnen frei zur Verfügung?",
		doc="We ask participants how much money they have freely available each month.")

