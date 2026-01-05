from odoo import models


class ReportMoOverview(models.AbstractModel):
    _inherit = 'report.mrp.report_mo_overview'

    def _get_report_data(self, production_id):
        return super(ReportMoOverview, self.sudo())._get_report_data(production_id)
