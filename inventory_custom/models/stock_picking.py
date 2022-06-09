# -*- coding: utf-8 -*-
#
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


#
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()

        if self.picking_type_code == 'outgoing':
            for x in self.move_ids_without_package:
                # avail_qty = self.env['stock.quant']._get_available_quantity(x.product_id, x.location_dest_id)
                qty = x.product_id.secondary_quantity
                if qty < x.quantity_2:
                    raise ValidationError(
                        _("Quantity 2 of Product %s must be less than or equal to %s") % (
                            x.product_id.display_name, qty))

        self.change_secondary_quantity()
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

        # @api.depend('quantity_done')
        # def get_test_uom(self):
        #     if self.quantity_done ==0 :
        #         quantity_2=0
        #


class ProductProduct(models.Model):
    _inherit = 'product.product'

    secondary_uom_id = fields.Many2one('uom.uom', string='Secondary Unit Of Measure')
    secondary_quantity = fields.Float('Secondary Quantity', readonly=True)

    @api.constrains("secondary_quantity", "qty_available")
    def check_secondary_quantity(self):
        for product in self:
            if product.secondary_quantity == 0 and product.qty_available != 0:
                raise ValidationError(
                    _("Secondary quantity of product %s must be positive when quantity available is not equal to zero") % product.display_name)
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
