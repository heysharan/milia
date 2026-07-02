import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    wo_qty_done = fields.Float(
        string='Qty Done',
        default=0.0,
        digits='Product Unit of Measure',
    )
    wo_qty_remaining = fields.Float(
        string='Qty Remaining',
        compute='_compute_wo_qty_remaining',
        store=True,
        digits='Product Unit of Measure',
    )

    @api.depends('wo_qty_done', 'qty_production')
    def _compute_wo_qty_remaining(self):
        for wo in self:
            wo.wo_qty_remaining = max(0.0, wo.qty_production - wo.wo_qty_done)

    def update_wo_qty_done(self, qty):
        """
        Called from shop floor JS.
        Sets wo_qty_done to the absolute qty value passed.
        """
        self.ensure_one()
        _logger.warning(f"AJW update_wo_qty_done: WO={self.id}, qty={qty}")
        self.wo_qty_done = min(qty, self.qty_production)
        return True