from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inter_categ_uom_id = fields.Many2one('uom.uom', string="Consume In")
    inter_categ_factor = fields.Float('Inter Category Factor')
    inter_categ_factor_inv = fields.Float('Inter Category Factor (Inverse)', compute='_compute_inter_categ_factor_inv')

    def _compute_inter_categ_factor_inv(self):
        for product_tmpl in self:
            product_tmpl.inter_categ_factor_inv = 1
            if product_tmpl.inter_categ_uom_id and product_tmpl.inter_categ_factor:
                product_tmpl.inter_categ_factor_inv = 1 / product_tmpl.inter_categ_factor
