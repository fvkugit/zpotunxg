{
    'name': 'Account Projection',
    'version': '15.0.1.0.0',
    'summary': 'Manage financial projections and link them to real accounting moves.',
    'depends': ['account', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/projection_link_wizard_views.xml',
        'views/projection_report_views.xml',
        'report/projection_report.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
