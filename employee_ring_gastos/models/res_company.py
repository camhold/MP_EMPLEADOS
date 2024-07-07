import re

from odoo import api, fields, models, SUPERUSER_ID
from odoo.tools.translate import _


class ResCompany(models.Model):
    _inherit = "res.company"

    account_active = fields.Many2one(
        "account.account",
        string="Cuentas de Activo",
        domain="[('user_type_id.type', 'in', ['receivable', 'liquidity', 'other'])]",
    )
    account_passive = fields.Many2one(
        "account.account",
        string="Cuentas de Pasivo",
        domain="[('user_type_id.type', 'in', ['payable', 'liquidity', 'other'])]",
    )
