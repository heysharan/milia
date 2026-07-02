from odoo import fields, models, api
from collections import defaultdict

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quantity_summary = fields.Char(
        string='Total Quantities',
        compute='_compute_quantity_summary',
    )

    @api.depends('order_line.product_uom_qty', 'order_line.product_uom')
    def _compute_quantity_summary(self):
        for order in self:
            totals = defaultdict(float)
            for line in order.order_line:
                if line.display_type:
                    continue
                if line.product_type == 'combo':
                    continue
                uom = line.product_uom.name or ''
                totals[uom] += line.product_uom_qty
            order.quantity_summary = '   |   '.join(
                f"{qty:g} {uom}" for uom, qty in totals.items()
            )

    def _get_quantity_by_uom(self):
        """For PDF report — returns list of (uom_name, qty) tuples."""
        totals = defaultdict(float)
        for line in self.order_line:
            if line.display_type:
                continue
            if line.product_type == 'combo':
                continue
            uom = line.product_uom.name or ''
            totals[uom] += line.product_uom_qty
        return list(totals.items())