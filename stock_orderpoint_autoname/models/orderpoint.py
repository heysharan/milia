from odoo import models, api


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.model
    def create(self, vals):
        # Auto-generate name if missing
        if not vals.get("name"):
            product = self.env["product.product"].browse(vals.get("product_id"))
            location = self.env["stock.location"].browse(vals.get("location_id"))

            if product and location:
                vals["name"] = f"{product.display_name} - {location.complete_name}"
            else:
                vals["name"] = "Reordering Rule"

        return super().create(vals)
