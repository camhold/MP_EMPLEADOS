import base64
from odoo import models, fields
import openpyxl
import io


class DataImportModel(models.TransientModel):
    _name = 'data.import.model'
    _description = 'Model is added to add excel csv file'

    attachment_name = fields.Char(string="Nombre archivo")
    attachment_file = fields.Binary(string="Archivo", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Compania", help="Company used for the import",
                                 default=lambda self: self.env.company, required=True, readonly=True)
    file_update = fields.Date(string='Fecha de Remuneracion', required=True)
    pwd = fields.Text()

    def action_import(self):
        return self._import_files()

    def _get_rows(self, attachment, attachment_name):
        file_content = io.BytesIO(base64.b64decode(self.attachment_file))
        workbook = openpyxl.load_workbook(file_content)
        sheet = workbook.active
        if not self.env['account.move'].sudo().search([
            ('name', 'ilike', f'REM/{self.file_update.year}/{self.file_update.month}%')
        ]):
            provision_move_ids = self.env['account.move'].sudo().search([('name', 'ilike', 'REM%')])
            current_date = self.file_update
            if not provision_move_ids:
                name = f"REM/{current_date.year}/{current_date.month}/1"
            else:
                name = f"REM/{current_date.year}/{current_date.month}/{len(provision_move_ids)}"

            journal_id = self.env['account.journal'].search([('is_remuneration', '=', True)], limit=1)
            account_move_id = self.env['account.move'].sudo().create({
                'state': 'draft',
                'date': self.file_update,
                'journal_id': journal_id.id,
                'name': name,
                'currency_id': self.env.company.currency_id.id
            })
            list_line_ids = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                account_id = self.env['account.account'].search([('code', '=', row[1])], limit=1)
                amount_currency = row[4] if (row[5] == 0 or row[5] is None) else row[5]
                amount_currency = amount_currency * -1 if row[5] != 0 else amount_currency
                last_digit = row[0][-1]
                line_id_to_add = (0, 0, {
                    'account_id': account_id.id,
                    'account_root_id': account_id.id,
                    'name': f'{row[0][:-1]}-{last_digit}',
                    'display_type': False,
                    'debit': row[4] if row[4] else 0,
                    'credit': row[5] if row[5] else 0,
                    'amount_currency': amount_currency,
                    'currency_id': self.env.company.currency_id.id,
                    'company_currency_id': self.env.company.currency_id.id,
                    'quantity': 1,
                    'product_id': False,
                })
                list_line_ids.append(line_id_to_add)
            account_move_id.sudo().write({'line_ids': list_line_ids})


    def _import_files(self, models=None):
         self._get_rows(self.attachment_file, self.attachment_name)
