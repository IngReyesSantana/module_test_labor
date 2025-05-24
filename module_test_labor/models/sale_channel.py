from odoo import fields, models, api


class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Sale Channel'

    name = fields.Char(
        string='Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE (code)', 'The code must be unique')
    ]