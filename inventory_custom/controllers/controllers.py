# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryCustom(http.Controller):
#     @http.route('/inventory_custom/inventory_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_custom/inventory_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_custom.listing', {
#             'root': '/inventory_custom/inventory_custom',
#             'objects': http.request.env['inventory_custom.inventory_custom'].search([]),
#         })

#     @http.route('/inventory_custom/inventory_custom/objects/<model("inventory_custom.inventory_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_custom.object', {
#             'object': obj
#         })
