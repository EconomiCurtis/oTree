# -*- coding: utf-8 -*-
import matrix_asymmetric.forms as forms
from matrix_asymmetric.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Decision(Page):

    template_name = 'matrix_asymmetric/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'rowAcolumnA_row': currency(self.treatment.rowAcolumnA_row),
            'rowAcolumnA_column': currency(self.treatment.rowAcolumnA_column),

            'rowAcolumnB_row': currency(self.treatment.rowAcolumnB_row),
            'rowAcolumnB_column': currency(self.treatment.rowAcolumnB_column),

            'rowBcolumnA_row': currency(self.treatment.rowBcolumnA_row),
            'rowBcolumnA_column': currency(self.treatment.rowBcolumnA_column),

            'rowBcolumnB_row': currency(self.treatment.rowBcolumnB_row),
            'rowBcolumnB_column': currency(self.treatment.rowBcolumnB_column),
        }

class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()


class Results(Page):

    template_name = 'matrix_asymmetric/Results.html'

    def variables_for_template(self):
        return {
            'payoff': currency(self.participant.payoff),
            'my_decision': self.participant.decision,
            'other_decision': self.participant.other_participant().decision,
            'same_decision': self.participant.decision == self.participant.other_participant().decision,
        }


def pages():
    return [
        Decision,
        ResultsWaitPage,
        Results
    ]