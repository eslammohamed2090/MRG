# -*- coding: utf-8 -*-
#
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


#
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        res = super(StockPicking, self)._action_done()

        for move in self.mapped("move_ids_without_package").filtered(lambda m: m.quantity_done != 0):
            if move.picking_code == "outgoing":
                qty = move.product_id.secondary_quantity
                if qty < move.quantity_2:
                    raise ValidationError(
                        _("Quantity 2 of Product %s must be less than or equal to %s") % (
                            move.product_id.display_name, qty))

                move.product_id.secondary_quantity = move.product_id.secondary_quantity - move.quantity_2
            elif move.picking_code == "incoming":
                move.product_id.secondary_quantity = move.product_id.secondary_quantity + move.quantity_2

        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    secondary_uom_id = fields.Many2one('uom.uom', string='Secondary Unit Of Measure')
    secondary_quantity = fields.Float('Secondary Quantity', readonly=True)

    @api.constrains("secondary_quantity", "qty_available")
    def check_secondary_quantity(self):
        for product in self:
            # if product.secondary_quantity == 0 and product.qty_available != 0:
            #     raise ValidationError(
            #         _("Secondary quantity of product %s must be positive when quantity available is not equal to zero") % product.display_name)
            if product.secondary_quantity != 0 and product.qty_available == 0:
                raise ValidationError(
                    _("Secondary quantity of product %s must be zero when quantity available is equal to zero") % product.display_name)


class StockMove(models.Model):
    _inherit = 'stock.move'

    secondary_uom_id = fields.Many2one('uom.uom', string='Secondary Unit Of Measure')
    quantity_2 = fields.Float('Quantity Done 2')

    @api.onchange('product_id')
    def onchange_secondary_uom(self):
        self.secondary_uom_id = self.product_id.secondary_uom_id

    @api.model
    def create(self, vals):
        res = super(StockMove, self).create(vals)
        if res.product_id.secondary_uom_id and not res.secondary_uom_id:
            res.write({"secondary_uom_id": res.product_id.secondary_uom_id.id})

        return res
