from odoo import fields, models


class MpGastos(models.Model):
    _name = "mp.gastos"
    _description = "Gastos de Empleados"

    concepto = fields.Text()
    monto = fields.Float()
    empleado_ext_id = fields.Integer()
    empleado_id = fields.Many2one(comodel_name='hr.employee')
    expense_ext_id = fields.Integer()
    estado = fields.Selection(
        selection=[
            ("aprobado", "Aprobado"),
            ("rechazado", "Rechazado"),
        ],
        string='Estado'
    )
    estado_recuperado = fields.Selection(
        selection=[
            ("recuperado", "Recuperado"),
            ("no_recuperado", "No recuperado"),
        ],
        string='Estado Recuperado',
        default='no_recuperado'
    )

    def reponer_fondos(self):
        for gasto_id in self:
            gasto_id.estado_recuperado = 'recuperado'
