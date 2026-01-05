from odoo import models, fields, api

class IrSequenceInherit(models.Model):
    _inherit = 'ir.sequence'


    active = fields.Boolean(default=False)

    @api.model
    def init(self):
        self.search([]).write({'active': False})