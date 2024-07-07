from odoo import models, fields


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    is_inventory = fields.Boolean(default=False, string='Es inventario?')
