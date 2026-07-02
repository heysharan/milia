from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    hidden_attribute_ids = fields.Many2many(
        'product.attribute',
        string='Hidden Attributes in Print',
        help="Attributes selected here will NOT appear on the printed Sale Order."
    )

    product_attribute_ids = fields.Many2many(
        'product.attribute',
        compute='_compute_product_attribute_ids',
        string='Product Attributes',
    )

    @api.depends('product_id')
    def _compute_product_attribute_ids(self):
        for line in self:
            if line.product_id:
                line.product_attribute_ids = (
                    line.product_id
                    .product_template_attribute_value_ids
                    .mapped('attribute_id')
                )
            else:
                line.product_attribute_ids = False

    def get_sale_order_line_multiline_description_sale(self):
        description = self.product_id.display_name or ''

        if self.product_id and self.product_id.product_template_attribute_value_ids:
            attrs = []
            for ptav in self.product_id.product_template_attribute_value_ids:
                if not ptav.attribute_id.print_on_sale_order:
                    continue
                if ptav.attribute_id in self.hidden_attribute_ids:
                    continue
                attrs.append(ptav.name)

            if attrs:
                description = self.product_id.product_tmpl_id.name + '\n' + ', '.join(attrs)
            else:
                description = self.product_id.product_tmpl_id.name

        if self.product_id.description_sale:
            description += '\n' + self.product_id.description_sale

        return description

    def _get_sale_order_line_name_for_portal(self):
        return self.get_sale_order_line_multiline_description_sale()