from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_active = fields.Many2one(
        related='company_id.account_active',
        string="Cuenta Activa",
    )
    account_passive = fields.Many2one(
        related='company_id.account_passive',
        string="Cuenta Pasiva",
    )
