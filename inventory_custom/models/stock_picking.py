# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for rec in self:
            if rec.picking_type_code != 'outgoing':
                rec.change_secondary_quantity()
                return res

            else:
                if any(line.quantity_done > line.product_id.qty_available for line in rec.move_ids_without_package):
                    raise ValidationError(_("Quantity Done Cannot be more than quantity available "))
                else:
                    rec.change_secondary_quantity()
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

    secondary_uom_id = fields.Many2one('uom.uom',string='Secondary Unit Of Measure')
    secondary_quantity = fields.Float('Secondary Quantity', )


class StockMove(models.Model):
    _inherit = 'stock.move'

    secondary_uom_id = fields.Many2one('uom.uom',string='Secondary Unit Of Measure')
    quantity_2 = fields.Float('Quantity Done 2')

    @api.onchange('product_id')
    def get_second_uom(self):
        for rec in self:
            rec.secondary_uom_id = rec.product_id.secondary_uom_id.id
