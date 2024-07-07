{
    'name': "Centralizacion Remuneraciones",
    'summary': """Se agrega la centralizacion de remuneracion por archivo XLS""",

    'author': "Tonny Velazquez",
    'website': "corner.store59@gmail.com",

    'category': 'employee',
    'version': '15.0.0.0.1',
    'depends': ['hr', 'account'],

    'data': [
        'data/mp_remisiones_secuence.xml',
        'security/ir.model.access.csv',
        'wizard/data_import_model_views.xml',
        'wizard/validate_wizard_views.xml',
        'views/hr_employee_views.xml',
        'views/account_move_views.xml',
        'views/account_journal_views.xml',
    ],
    "license": "Other proprietary",
}
