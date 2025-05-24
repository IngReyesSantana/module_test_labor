from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    number_customer = fields.Char(
        string='Number Customer',
        help='Customer number assigned by the external system',
    )
