from odoo import models

class StockRule(models.Model):
    _inherit = 'stock.rule'


    def _should_auto_confirm_procurement_mo(self, p):
        return False