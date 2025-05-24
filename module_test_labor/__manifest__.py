# -*- coding: utf-8 -*-
{
    'name': "Modulo Prueba Mirgor",

    'summary': """
        module test Mirgor,
    """,

    'description': """
        Modulo para la Prueba Test Mirgor
    """,

    'author': "Reyes Hernando Santana Perez - inghernandosan@gmail.com",
    'website': "https://odoo.com",

    'category': 'Operations',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'sale_management',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/report_sale_quota.xml',
        'views/res_partner.xml',
        'views/sale_channel.xml',
        'views/sale_order.xml',
        'views/sale_quota.xml',
    ],

    'application': False,
    'license': 'LGPL-3',
}
