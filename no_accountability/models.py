from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Luisa Kling, Christian König-Kersting, Stefan T. Trautmann'

doc = """
Risk Taking for Others Experiment 2018, no accountability treatment
"""


def make_empathy_question(label):
    return models.IntegerField(
        choices=[(1,''), (2, ''), (3, ''), (4, '')],
        label=label,
        widget=widgets.RadioSelect
    )


class Constants(BaseConstants):
    name_in_url = 'no_accountability'
    players_per_group = 2
    num_rounds = 1

    duration = 30

    endowment_principals = c(10)

    # Fixed Compensation
    fixed_payment = c(5)

    # Variable Compensation
    share_result = 25  # In Prozent
    share_profit = 35


class Subsession(BaseSubsession):

    def creating_session(self):
        random_number = random.randint(1, 2)
        for player in self.get_players():
            player.compensation = self.session.config["compensation"]
            player.participation_fee = self.session.config["participation_fee"]
            player.random_number = random_number



class Group(BaseGroup):
    investment_success = models.BooleanField(
        doc="Turns true if the investment was successful and 0 in case it was not.")

    def after_investments(self):
        self.investment_success = (random.random() <= 1 / 3)
        for player in self.get_players():
            if player.role() == "Principal":
                player.get_investment()
                player.calculate_payoffs_principals()

            if player.role() == "Agent":
                player.get_payoff_profit()
                player.calculate_payoffs_agents()


class Player(BasePlayer):
    random_number = models.IntegerField(
        doc="Turns either 1 or 2 (see subsession) and is used to randomly assign roles in the experiment (see def role).")

    compensation = models.CharField(doc="Compensation scheme put in place for agents (see Settings).")

    participation_fee = models.CurrencyField(doc="Participation fee for all agents (can be modified in Settings).")

    def role(self):
        return "Principal" if self.id_in_group == self.random_number else "Agent"


    # Everyone takes the investment decision for their principal:

    decision_for_p1 = models.CurrencyField(
        min=0,
        max=Constants.endowment_principals,
        widget=widgets.Slider(),  # Neuer Slider von Christian
        verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
        doc="Agents investment for the principal in the risky asset.")

    investment = models.CurrencyField(doc="Indicates for everyone the investment decision as taken by their agents.")

    def get_investment(self):
        agent = self.get_others_in_group()[0]
        self.investment = agent.decision_for_p1


    # Payoffs:
    def calculate_payoffs_principals(self):
        if self.role() == "Principal":
            if self.group.investment_success:
                self.payoff = self.investment * 3.5 + (Constants.endowment_principals - self.investment)
                self.profit = self.investment * 2.5
            else:
                self.payoff = Constants.endowment_principals - self.investment
                self.profit = 0

    profit = models.CurrencyField(doc="Gives the profit of the principal.")

    payoff_of_principal = models.CurrencyField(doc="Gives for each agent the payoff of his principal.")
    profit_of_principal = models.CurrencyField(doc="Gives for each agent the payoff of his principal.")

    def get_payoff_profit(self):
        principal = self.get_others_in_group()[0]
        self.profit_of_principal = principal.profit
        self.payoff_of_principal = principal.payoff

    def calculate_payoffs_agents(self):
        if self.role() == "Agent":
            if self.compensation == "fixed":
                self.payoff = Constants.fixed_payment
            if self.compensation == "variable_result":
                self.payoff = Constants.fixed_payment + Constants.share_result / 100 * self.payoff_of_principal
            if self.compensation == "variable_profit":
                self.payoff = Constants.fixed_payment + Constants.share_profit / 100 * self.profit_of_principal

    # Comprehension Questions (Instructions 1)
    question_1 = models.CharField(
        widget=widgets.RadioSelectHorizontal(),
        choices=["Richtig", "Falsch"])

    question_2 = models.CharField(
        widget=widgets.RadioSelectHorizontal(),
        choices=["Richtig", "Falsch"])

    # Comprehension questions instructions 2
    question_3 = models.CurrencyField()
    question_4 = models.CurrencyField()

    # comprehension question instructions 3
    question_6 = models.CharField(widget=widgets.RadioSelectHorizontal(), choices=["Richtig", "Falsch"])


    # Questionnaire:
    age = models.PositiveIntegerField(
        max=100,
        verbose_name="Wie alt sind Sie?",
        doc="We ask participants for their age between 0 and 100 years")

    gender = models.CharField(
        choices=["männlich", "weiblich", "anderes"],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Was ist Ihr Geschlecht?",
        doc="gender indication")

    studies = models.CharField(
        blank=True,
        verbose_name="Was studieren Sie im Hauptfach?",
        doc="field of studies indication.")

    nonstudent = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name="Kein Student",
        doc="Ticking the checkbox means that the participant is a non-student.")

    financial_advice = models.BooleanField(
        choices=[(True, "Ja"), (False, "Nein")],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name="Haben Sie bereits eine Bankberatung in Anspruch genommen?",
        doc="We ask participants if they ever made use of financial advice.")

    income = models.CurrencyField(
        verbose_name="Wie viel Geld im Monat steht Ihnen frei zur Verfügung?",
        doc="We ask participants how much money they have freely available each month.")

    # empathy questions
    em1 = make_empathy_question("Ich erkenne leicht, ob jemand ein Gespräch anfangen möchte.")
    em2 = make_empathy_question("Ich bemerke leicht, wenn jemand etwas anderes sagt, als er meint.")
    em3 = make_empathy_question("Es fällt mir leicht mich in einen anderen Menschen hineinzuversetzen.")
    em4 = make_empathy_question("Ich kann gut vorhersagen, wie jemand sich fühlen wird.")
    em5 = make_empathy_question("Ich bemerke schnell, wenn jemand sich unbehaglich oder unwohl in einer Gruppe fühlt.")
    em6 = make_empathy_question(
        "Andere Leute bestätigen, dass ich gut nachempfinden kann, was andere denken oder fühlen.")
    em7 = make_empathy_question(
        "Ich erkenne leicht, ob jemand das, was ich erzähle, interessant oder langweilig findet.")
    em8 = make_empathy_question(
        "Freunde erzählen mir normalerweise von ihren Problemen, weil sie mich für besonders verständnisvoll halten.")
    em9 = make_empathy_question("Ich bemerke, wenn ich störe, auch wenn die andere Person es nicht sagt.")
    em10 = make_empathy_question(
        "Ich kann mich schnell und intuitiv darauf einstellen, wie eine andere Person sich fühlt.")
    em11 = make_empathy_question(
        "Es fällt mir leicht herauszufinden, worüber mein Gesprächspartner sich gerne unterhalten möchte.")
    em12 = make_empathy_question("Ich erkenne, ob jemand seine wahren Gefühle verbirgt.")
    em13 = make_empathy_question("Ich kann gut vorhersagen, was jemand tun wird.")

    em_score = models.IntegerField()

    def score_empathy(self):
        # transformation is as follows:
        # 1 and 2 become 0,
        # 3 becomes 1,
        # 4 becomes 2

        # that is: substract 2, then check if value is negative. if so, set to 0 instead.

        # these are then summed up
        raw_scores = [
            self.em1, self.em2, self.em3, self.em4, self.em5, self.em6, self.em7, self.em8, self.em9, self.em10, self.em11, self.em12, self.em13
        ]

        transformed_scores = []

        for score in raw_scores:
            transformed = score - 2
            transformed = 0 if transformed < 0 else transformed

            transformed_scores.append(transformed)

        self.em_score = sum(transformed_scores)



    # Dummies für Stata:

    female = models.BooleanField(
        doc="Turns True if the participant is a woman."
    )

    male = models.BooleanField(
        doc="Turns True if the participant is a man."
    )

    other_gender = models.BooleanField(
        doc="Turns True if the participant indicates other."
    )

    econ_student = models.BooleanField(
        doc="Turns True if the participant is an economics student."
    )


    def create_gender_dummies(self):
        if self.gender == "weiblich":
            self.female = True
            self.male = False
            self.other_gender = False
        elif self.gender == "männlich":
            self.female = False
            self.male = True
            self.other_gender = False
        elif self.gender == "anderes":
            self.female = False
            self.male = False
            self.other_gender = True

    def create_econ_dummy(self):
        if self.studies:
            subject = self.studies.lower()
            if "econ" in subject:
                self.econ_student = True
            elif "vwl" in subject:
                self.econ_student = True
            elif "ökono" in subject:
                self.econ_student = True
            else:
                self.econ_student = False
        else:
            self.econ_student = False

