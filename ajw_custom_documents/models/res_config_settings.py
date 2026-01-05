from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    msme_cert_expiry_notify_before = fields.Integer(string="MSME Notify Before",config_parameter='ajw_custom_documents.msme_cert_expiry_notify_before')