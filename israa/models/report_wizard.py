from odoo import fields, models, api


class helpWizard(models.TransientModel):
    _name = 'help.wizard'
    _rec_name = ''
    team = fields.Char(
        string='Team',
        required=False)

    state = fields.Selection(
        string='State',
        selection=[('new', 'New'),
                   ('in progress', 'In Progress'), ('solved', 'Solved'), ('cancel', 'Cancel')],
        required=False)

    state_tick = fields.Boolean(string='With state', required=False)

    def generate_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'team': self.team,
                'state': self.state,
                'state_tick': self.state_tick

            },
        }
        return self.env.ref('israa.action_report_helpdesk').report_action(self, data=data)


class VisitDateReport(models.AbstractModel):
    _name = 'report.israa.report_helpdesk_temp'

    @api.model
    def _get_report_values(self, docs, data=None):
        team = data['form']['team']
        state = data['form']['state']
        state_tick = data['form']['state_tick']
        docs = []
        help_details = []
        help_all = []

        # docs = self.env['hd.ticket'].search([('team', 'is', True),
        #                                      ('state', 'in', ('new', 'solve', 'in progress'))])
        docs = self.env['hd.ticket'].search([])
        if state_tick:
            docsnames = docs.mapped('team')
            docsnames = set(docsnames)
            for name in docsnames:
                filtered_records = docs.filtered(lambda m: m.team == name)
                help_details.append(
                    {'name': name.name, 'ticket_id': name.ticket_id, 'resolution_time': name.resolution_time,
                     'time_submitted': name.time_submitted, 'priority': name.priority})
            print("help detailllls", help_details)
        if not state_tick:
            for name in docs:
                help_all.append(
                    {'name': name.name, 'ticket_id': name.ticket_id, 'resolution_time': name.resolution_time,
                     'time_submitted': name.time_submitted, 'priority': name.priority})
                print("help alllss", help_all)

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'team': team,
            'state_tick': state_tick,
            'help_details': help_details,
            'help_all': help_all,
        }
