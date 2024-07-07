from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.sql_db import db_connect


class Employee(models.Model):
    _inherit = 'hr.employee'

    accounting_state = fields.Selection(
        selection=[("not_account", "No contabilizado"), ("account", "Contabilizado")],
        default="not_account", string="Estado de contabilizacion"
    )
    account_date = fields.Date(string='Fecha de cotabilizacion')
    amount_account_auth = fields.Monetary(string='Fondo Fijo Autorizado', currency_field="company_currency_id", default=0)
    amount_account = fields.Monetary(string='Fondo Fijo Saldo', currency_field="company_currency_id", default=0)
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency of the Payment Transaction",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    move_id = fields.Many2one(comodel_name='account.move', string='Entrada de diario')
    qty_to_approve = fields.Float(string='Cantidad a aprobar', default=0)
    document_approve = fields.Selection(selection=[
        ("solicitud_presupuesto", "Solicitudes de Presupuesto"),
        ("orden_compra", "Orden de Compra")
    ], string='Documento a Aprobar')

    def _compute_amount_account(self):
        for employee_id in self:
            other_db = db_connect('PROCESOS')
            try:
                with other_db.cursor() as other_db_cursor:
                    other_db_cursor.execute(f"SELECT * FROM mp_usuarios WHERE email = '{employee_id.work_email}'")
                    result = other_db_cursor.fetchall()
                    if not result:
                        employee_id.amount_account = 0
                    else:
                        if result[0][-1] == '-1':
                            employee_id.amount_account = 0
                        else:
                            gastos_ids = self.env['mp.gastos'].search([('empleado_ext_id', '=', result[0][1])])
                            amount_total = 0
                            for gasto_id in gastos_ids:
                                if gasto_id.estado_recuperado == 'no_recuperado':
                                    amount_total += gasto_id.monto
                            employee_id.amount_account = employee_id.amount_account_auth - amount_total

            except Exception:
                employee_id.amount_account = 0
    def validate_fixed_asset(self):
        employee_ids = self.env['hr.employee'].search([('accounting_state', '=', 'not_account')])
        currency_clp_id = self.env.ref('base.CLP')
        amount_total = 0
        active_account_id = self.env.user.company_id.account_active
        active_passive_id = self.env.user.company_id.account_passive
        if not active_passive_id:
            raise UserError(_("Se debe de tener una cuenta pasiva para el FONDO FIJO."))
        if not active_account_id:
            raise UserError(_("Se debe de tener una cuenta activa para el FONDO FIJO."))
        for employee_id in employee_ids:
            amount_total += employee_id.amount_account
        journal_id = self.env['account.journal'].search([('code', 'ilike', 'vario')])
        current_date = fields.Datetime.now()
        account_move_id = self.env['account.move'].sudo().create({
            'state': 'draft',
            'date': fields.Datetime.now(),
            'journal_id': journal_id.id,
            'name': self.env["ir.sequence"].next_by_code("FF"),
            'currency_id': currency_clp_id.id
        })
        list_line_ids = []
        account_list = [active_passive_id, active_account_id]
        debit = False
        for account_id in account_list:
            line_id_to_add = (0, 0, {
                'account_id': account_id.id,
                'account_root_id': account_id.id,
                'name': account_id.name,
                'display_type': False,
                'debit': amount_total if debit else 0,
                'credit': 0 if debit else amount_total,
                'amount_currency': amount_total,
                'currency_id': currency_clp_id.id,
                'company_currency_id': self.env.company.currency_id.id,
                'quantity': 1,
                'product_id': False,
            })
            debit = True
            list_line_ids.append(line_id_to_add)
        account_move_id.sudo().write({'line_ids': list_line_ids})
        account_move_id.sudo().write({'date': current_date})
        account_move_id.action_post()
        for employee_id in employee_ids:
            employee_id.move_id = account_move_id
            employee_id.accounting_state = 'account'

