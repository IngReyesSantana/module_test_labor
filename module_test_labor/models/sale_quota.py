from odoo import fields, models, api


class SaleQuota(models.Model):
    _name = 'sale.quota'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Quota'

    sale_channel_id = fields.Many2one(
        comodel_name='sale.channel',
        string='Sale Channel',
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
    )
    star_date = fields.Date(
        string='Start Date',
        required=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
    )
    sale_quote = fields.Integer(
        string='Sale Quota',
        required=True,
    )
    quantity_sold = fields.Integer(
        string='Quantity Sold',
    )
    available_quantity = fields.Integer(
        string='Available Quantity',
        compute='_compute_available_quantity',
    )

    @api.depends('sale_quote', 'quantity_sold')
    def _compute_available_quantity(self):
        for record in self:
            record.available_quantity = record.sale_quote - record.quantity_sold

    def get_sale_orders(self):
        order_line = self.env['sale.order.line']
        results = []
        for quota in self:
            lines = order_line.search([
                ('product_id', '=', quota.product_id.id),
                ('order_id.partner_id', '=', quota.partner_id.id),
                ('order_id.sale_channel_id', '=', quota.sale_channel_id.id),
                ('order_id.date_order', '>=', quota.star_date),
                ('order_id.date_order', '<=', quota.end_date),
                ('order_id.state', 'in', ['sale', 'done']),
            ])
            for line in lines:
                results.append({
                    'order_name': line.order_id.name,
                    'quantity': line.product_uom_qty,
                })
        return results

    def print_quota_report(self):
        return self.env.ref(
            'module_test_labor.report_sale_quota_print').report_action(self)
