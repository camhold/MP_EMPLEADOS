{
    'name': "Employee Ring Gastos",

    'summary': """Fields are added to the employees module for the adaptation of the Expense Ring API""",

    'author': "Tonny Velazquez",
    'website': "corner.store59@gmail.com",
    'category': 'Employee',
    'version': '15.0.0.0.1',
    'depends': ['base', 'hr', 'base_setup', 'account',
        'base_vat',
        'base_address_extended',
        'base_address_city',
        'l10n_latam_base',
        'l10n_latam_invoice_document',
        'account_debit_note',],
    'data': [
        'data/data.xml',
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/res_company_views.xml',
        # 'views/res_config_settings_views.xml',
        # 'views/templates.xml',
    ],
}
