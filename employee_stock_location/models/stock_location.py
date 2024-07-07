from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = 'stock.location'

    employee_id = fields.Many2one(comodel_name='hr.employee', string="Empleado")
    identification_id = fields.Char(related='employee_id.identification_id')
    is_employee = fields.Boolean(string='Es Empleado?', default=False)

    @api.onchange('is_employee', 'employee_id')
    def _set_name_employee_on_location(self):
        for stock_location_id in self:
            if stock_location_id.is_employee and stock_location_id.identification_id is not False:
                stock_location_id.name = stock_location_id.identification_id + '-' + stock_location_id.employee_id.name
                stock_location_id.employee_id.location_id = self._origin.id
                stock_location_id.employee_id.is_transit_location = True
            else:
                stock_location_id.name = False

    @api.model
    def create(self, vals):
        stock_location_id = super(StockLocation, self).create(vals)
        if stock_location_id.is_employee:
            employee_id = self.env['hr.employee'].browse(vals['employee_id'])
            if employee_id:
                if not employee_id.location_id:
                    employee_id.location_id = stock_location_id.id
                else:
                    raise ValidationError(_("Esté empleado ya tiene una ubicación de transito asignada"))
        return stock_location_id
