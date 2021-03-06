# -*- coding: utf-8 -*-
from __future__ import division
from otree import widgets
from otree.db import models
from otree.common import Currency as c, currency_range
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree_redwood.models import Decision

import random

doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class Constants(BaseConstants):
    name_in_url = 'discrete_bimatrix'
    players_per_group = 2
    num_rounds = 10

    # p1 payoffs
    p1_A_p2_A_amount = 800
    p1_A_p2_B_amount = 0
    p1_B_p2_A_amount = 0
    p1_B_p2_B_amount = 200

    # p2 payoffs
    p2_A_p1_A_amount = 0
    p2_A_p1_B_amount = 200
    p2_B_p1_A_amount = 200
    p2_B_p1_B_amount = 0

    base_points = 0

    # Amount of time the game stays on the decision page in seconds
    period_length = 600

    training_1_choices = [
        'Alice gets 300 points, Bob gets 0 points',
        'Alice gets 200 points, Bob gets 200 points',
        'Alice gets 0 points, Bob gets 300 points',
        'Alice gets 100 points, Bob gets 100 points'
    ]

    training_1_correct = training_1_choices[0]


class Subsession(BaseSubsession):
    def before_session_starts(self):
        self.group_randomly()


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    def is_training_question_1_correct(self):
        return self.training_question_1 == Constants.training_1_correct

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        self.decisions_over_time = Decision.objects.filter(
                component='otree-bimatrix',
                session=self.session,
                subsession=self.subsession.name(),
                round=self.round_number,
                group=self.group.id_in_subsession)

        payoff = 0

        # default state when no decisions have been made
        my_state = .5
        other_state = .5

        if (self.id_in_group == 1):
            A_A_payoff = Constants.p1_A_p2_A_amount
            A_B_payoff = Constants.p1_A_p2_B_amount
            B_A_payoff = Constants.p1_B_p2_A_amount
            B_B_payoff = Constants.p1_B_p2_B_amount
        else:
            A_A_payoff = Constants.p2_A_p1_A_amount
            A_B_payoff = Constants.p2_A_p1_B_amount
            B_A_payoff = Constants.p2_B_p1_A_amount
            B_B_payoff = Constants.p2_B_p1_B_amount

        for i, change in enumerate(self.decisions_over_time):
            if change.participant == self.participant:
                my_state = change.value
            else:
                other_state = change.value

            if my_state != None and other_state != None:
                if my_state == 0:
                    if other_state == 0:
                        cur_payoff = A_A_payoff / Constants.period_length
                    else:
                        cur_payoff = A_B_payoff / Constants.period_length
                else:
                    if other_state == 0:
                        cur_payoff = B_A_payoff / Constants.period_length
                    else:
                        cur_payoff = B_B_payoff / Constants.period_length

                if i == len(self.decisions_over_time) - 1:
                    next_change_time = self.session.vars['end_time_{}'.format(self.group.id_in_subsession)]
                else:
                    next_change_time = self.decisions_over_time[i + 1].timestamp

                payoff += (next_change_time - change.timestamp).total_seconds() * cur_payoff

        self.payoff = payoff

