from datetime import date

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_channel_id = fields.Many2one(
        comodel_name='sale.channel',
        string='Sale Channel',
        required=True,
    )

    def action_confirm(self):
        today = date.today()
        for order in self:
            for line in order.order_line:
                product = line.product_id
                quantity_to_sell = line.product_uom_qty
                channel = order.sale_channel_id
                customer = order.partner_id
                quotas = self.env['sale.quota'].search([
                    ('product_id', '=', product.id),
                    ('sale_channel_id', '=', channel.id),
                    ('partner_id', '=', customer.id),
                    ('star_date', '<=', today),
                    ('end_date', '>=', today),
                ], order='available_quantity desc')
                if quotas:
                    qty_remaining = quantity_to_sell
                    for quota in quotas:
                        if quota.available_quantity <= 0:
                            continue
                        assign_qty = min(qty_remaining,
                                         quota.available_quantity)
                        quota.quantity_sold += assign_qty
                        qty_remaining -= assign_qty
                        if qty_remaining == 0:
                            break
                    if qty_remaining > 0:
                        raise ValidationError(_(
                            "The sale cannot be confirmed because it exceeds "
                            "the available quota for product %s."
                        ) % product.name)
        return super().action_confirm()
