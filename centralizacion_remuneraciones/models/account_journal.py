from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_remuneration = fields.Boolean(string='Es diario para remuneraciones?')
