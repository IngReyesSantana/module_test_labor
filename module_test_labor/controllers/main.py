# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import http
from odoo.http import request


class SaleQuotaAPI(http.Controller):
    @http.route('/api/sale_quota', type='json', auth='public',
                methods=['POST'], csrf=False)
    def create_sale_quota(self, **kwargs):
        data = request.jsonrequest
        required_fields = [
            'codigo_canal',
            'sku_producto',
            'numero_cliente',
            'fecha_inicio',
            'fecha_fin',
            'cupo'
        ]
        for field in required_fields:
            if field not in data:
                return {"status": 400,
                        "error": f"Missing required field: {field}"}
        channel = request.env['sale.channel'].sudo().search(
            [('code', '=', data['codigo_canal'])], limit=1)
        if not channel:
            return {"status": 400,
                    "error": f"The sales channel with the code "
                             f"was not found. {data['codigo_canal']}."}
        product = request.env['product.template'].sudo().search(
            [('default_code', '=', data['sku_producto'])], limit=1)
        if not product:
            return {"status": 400,
                    "error": f"The product with SKU was not "
                             f"found. {data['sku_producto']}."}
        partner = request.env['res.partner'].sudo().search(
            [('number_customer', '=', data['numero_cliente'])], limit=1)
        if not partner:
            return {"status": 400,
                    "error": f"The customer with number was "
                             f"not found. {data['numero_cliente']}."}
        try:
            start_date = datetime.strptime(data['fecha_inicio'],
                                           '%Y-%m-%d').date()
            end_date = datetime.strptime(data['fecha_fin'],
                                         '%Y-%m-%d').date()
            cupo = int(data['cupo'])
            request.env['sale.quota'].sudo().create({
                'sale_channel_id': channel.id,
                'product_id': product.id,
                'partner_id': partner.id,
                'star_date': start_date,
                'end_date': end_date,
                'sale_quote': cupo,
                'quantity_sold': 0,
            })
            return {
                "status": 200,
                "mensaje": "Sales quota created successfully."
            }
        except Exception as e:
            return {"status": 400,
                    "error": f"Error processing the request: {str(e)}"}
