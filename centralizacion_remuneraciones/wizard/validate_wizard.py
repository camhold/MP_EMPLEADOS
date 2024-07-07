from odoo import models, fields
from odoo.tools.config import config
from odoo.exceptions import AccessError


class ValidateWizard(models.TransientModel):
    _name = 'validate.wizard'
    _description = 'validate wizard'

    pwd = fields.Text()

    def action_import(self):
        if config.get("rem_pwd") == self.pwd:
            action = self.env.ref(
                'centralizacion_remuneraciones.action_view_account_move_remuneraciones_view'
            ).read()[0]
            return action
        else:
            raise AccessError("Contrasenia incorrecta.")
