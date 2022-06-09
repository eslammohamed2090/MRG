# -*- coding: utf-8 -*-
#
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self.change_secondary_quantity()
        for x in self.move_ids_without_package:
            # avail_qty = self.env['stock.quant']._get_available_quantity(x.product_id, x.location_dest_id)
            qty = x.product_id.qty_available
            if not qty:
                x.quantity_2 = 0
                x.product_id.secondary_quantity = 0
        return res

    def change_secondary_quantity(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                if picking.picking_type_code == 'outgoing':
                    move.product_id.secondary_quantity = move.product_id.secondary_quantity - move.quantity_2
                elif picking.picking_type_code == 'incoming':
                    move.product_id.secondary_quantity = move.product_id.secondary_quantity + move.quantity_2
                else:
                    continue


class ProductProduct(models.Model):
    _inherit = 'product.product'

    secondary_uom_id = fields.Many2one('uom.uom', string='Secondary Unit Of Measure')
    secondary_quantity = fields.Float('Secondary Quantity', )


class StockMove(models.Model):
    _inherit = 'stock.move'

    secondary_uom_id = fields.Many2one('uom.uom', string='Secondary Unit Of Measure')
    quantity_2 = fields.Float('Quantity Done 2')

    @api.onchange('product_id')
    def get_second_uom(self):
        for rec in self:
            rec.secondary_uom_id = rec.product_id.secondary_uom_id.id
