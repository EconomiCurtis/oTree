# -*- coding: utf-8 -*-
import stackelberg_competition.forms as forms
from stackelberg_competition.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Introduction(Page):

    template_name = 'stackelberg_competition/Introduction.html'

    def variables_for_template(self):
        return {
            'total_capacity': self.treatment.total_capacity
        }


class ChoiceOne(Page):

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 1

    template_name = 'stackelberg_competition/ChoiceOne.html'

    def get_form_class(self):
        return forms.QuantityForm


class ChoiceTwo(Page):

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 2

    template_name = 'stackelberg_competition/ChoiceTwo.html'

    def get_form_class(self):
        return forms.QuantityForm

    def variables_for_template(self):
        return {
            'other_quantity': self.participant.other_participant().quantity
        }

class ResultsWaitPage(MatchWaitPage):
    def action(self):
        for p in self.match.participants():
            p.set_payoff()

class Results(Page):

    template_name = 'stackelberg_competition/Results.html'

    def variables_for_template(self):

        return {
            'payoff': currency(self.participant.payoff),
            'quantity': self.participant.quantity,
            'other_quantity': self.participant.other_participant().quantity,
            'price': currency(self.match.price)
        }


def pages():
    return [
        Introduction,
        ChoiceOne,
        MatchWaitPage,
        ChoiceTwo,
        ResultsWaitPage,
        Results
    ]