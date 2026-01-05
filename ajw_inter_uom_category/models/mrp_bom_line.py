from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    inter_categ_uom_qty = fields.Float('Qty to Consume')
    inter_categ_uom_id = fields.Many2one(related='product_id.inter_categ_uom_id')

    @api.onchange('inter_categ_uom_qty')
    def _onchange_inter_categ_uom_qty(self):
        self.product_qty = self.inter_categ_uom_qty * self.product_id.inter_categ_factor_inv
