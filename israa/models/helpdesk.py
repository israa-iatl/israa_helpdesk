from odoo import fields, models, api
from datetime import datetime, timedelta


class Teams(models.Model):
    _name = 'hd.team'
    _description = 'Description'

    name = fields.Char(string="Name")


class Tickets(models.Model):
    _name = 'hd.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Name',
        required=False)

    # automatic creation of ticket id
    @api.model
    def create(self, vals):
        if vals.get('ticket_id', _('New')) == _('New'):
            # vals['ticket_id'] = self.env['ir.sequence'].next_by_code(
            #     'ticket_id') or 'New'
            vals['ticket_id'] = self.env['ir.sequence'].next_by_code(
                'ticket_id') or '"%S" + team_id + "/ NO."'
        result1 = super(Tickets, self).create(vals)
        return result1

    ticket_id = fields.Char(string='Ticket Id', default=lambda self: _('New'), copy=False)

    description = fields.Text(
        string="Description",
        required=False)
    team_id = fields.Many2one(
        comodel_name='hd.team',
        string='Team',
        required=False)
    assigned_to_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned To',
        required=False)
    priority = fields.Selection(
        string='Priority ',
        selection=[('Low', 'low'),
                   ('Medium', 'medium'), ('High', 'high'), ],
        required=False, )
    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True)
    customer_name = fields.Char(
        string='Customer_name', related='customer_id.name',
        required=False)
    customer_phone = fields.Char(
        string='Customer_phone', related='customer_id.phone',
        required=False)
    customer_email = fields.Char(
        string='Customer_email', related='customer_id.email',
        required=False)

    time_submitted = fields.Date(
        string='Time Submitted',
        readonly=True)
    tag_id = fields.Many2many(
        comodel_name='helpdesk.tag',
        string='Tags')
    host_type = fields.Selection(
        string='Hosting Type',
        selection=[('on-promise', 'On-promise'),
                   ('Cloud', 'Cloud'), ],
        required=True, )
    server_url = fields.Char(
        string='Server Url',
        required=False)

    # computaion of resolutiontime

    @api.depends('time_submitted')
    def calc_resolution(self):
        fmt = '%Y-%m-%d'
        start_date = self.customer_id.create_date
        end_date = self.time_submitted
        d1 = datetime.strptime(start_date, fmt)
        d2 = datetime.strptime(end_date, fmt)
        date_difference = d2 - d1
        return date_difference

    resolution_time = fields.Date(
        string='Resolution_time', compute='calc_resolution',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'),
                   ('in progress', 'In Progress'), ('solved', 'Solved'), ('cancel', 'Cancel')],
        required=False, default='new')

    def action_solve(self):
        self.state = 'solved'

    def action_in_progress(self):
        self.state = 'in_progress'

    def action_new(self):
        self.state = 'new'

    def action_cancel(self):
        self.state = 'cancel'


class ResPartner(models.Model):
    _inherit = 'res.partner'

    _columns = {
        'create_date': fields.datetime('Create Date', readonly=True),
    }
