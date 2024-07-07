from odoo import models, fields
from odoo.exceptions import AccessError


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_locked = fields.Boolean(compute='compute_access_account_move')

    def compute_access_account_move(self):
        for move_id in self:
            default_permission = self.env.context.get("default_permission")
            if move_id.name and move_id.name.startswith('REM/') and not default_permission:
                raise AccessError("No tienes permisos para desbloquear registros.")
            move_id.is_locked = False
