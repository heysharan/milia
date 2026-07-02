from odoo import fields, models

class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    print_on_sale_order = fields.Boolean(
        string='Print on Sale Order',
        default=True,
        help="If unchecked, this attribute will be hidden from the Sale Order PDF and customer portal."
    )