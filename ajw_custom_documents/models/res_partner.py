from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    msme_type = fields.Selection(
        selection=[
            ('micro', 'Micro'),
            ('small', 'Small'),
            ('medium', 'Medium'),
        ], store=True,
        string='MSME Type',
        help="Select the type of MSME."
    )

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)

        if 'msme_type' in vals and vals['msme_type']:
            self._create_document_request(partner)

        return partner

    def write(self, vals):
        res = super(ResPartner, self).write(vals)

        if 'msme_type' in vals and vals['msme_type']:
            for record in self:
                self._create_document_request(record)

        return res

    def _create_document_request(self, partner):
        existing_request = self.env['documents.request_wizard'].search([
            ('partner_id', '=', partner.id),
        ], limit=1)

        if not existing_request:

            default_folder = self.env['documents.document'].search([('name', '=', 'MSME Certificates')], limit=1)
            if default_folder:
                request_wizard = self.env['documents.request_wizard'].create({
                    'name': f"Document Request for {partner.name}",
                    'requestee_id': self.env.user.partner_id.id,
                    'partner_id': partner.id,
                    'folder_id': default_folder.id,
                    'activity_type_id': self.env.ref('documents.mail_documents_activity_data_md').id,
                })
                request_wizard.request_document()