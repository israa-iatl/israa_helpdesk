# -*- coding: utf-8 -*-
{
    'name': "helpdesk_custom",

    'summary': """
        Israa_abdelraheem""",

    'description': """
        helpdesk for handling teams and tickets.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'sequence': 1,

    # any module necessary for this one to work correctly
    'depends': ['helpdesk', 'base','mail', 'board'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/wizard.xml',
        'views/helpdesk.xml',
        'views/ticket_report.xml',
        'views/dashboard.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
