from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    location_id = fields.Many2one(comodel_name='stock.location', string='Ubicación de Transito', default=False)
    is_transit_location = fields.Boolean(string='Es Ubicación de Transito', default=False, copy=False)

    @api.model
    def create(self, vals):
        employee_id = super(HrEmployee, self).create(vals)
        if 'is_transit_location' in vals and 'location_id' not in vals:
            vals['location_id'] = self.env['stock.location'].create({
                'name': vals['identification_id'] + '-' + vals['name'],
                'usage': 'transit',
                'is_employee': True,
                'employee_id': employee_id.id,
            })
        return employee_id

    @api.onchange('location_id')
    def create_transit_location_relation(self):
        for employee_id in self:
            stock_location_id = self.env['stock.location'].browse(employee_id.location_id.id)
            if employee_id.location_id:
                stock_location_id.is_employee = True
                stock_location_id.employee_id = self._origin.id
