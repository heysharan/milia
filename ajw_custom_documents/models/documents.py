from datetime import timedelta, date
from odoo import models, fields
from odoo.exceptions import UserError


class Document(models.Model):
    _inherit = 'documents.document'

    expiry_date = fields.Date('Expiry Date')


    def mail_reminder(self):
        date_now = date.today()
        notify_before = int(
            self.env['ir.config_parameter'].sudo().get_param('ajw_custom_documents.msme_cert_expiry_notify_before', default=0)
        )

        if notify_before <= 0:
            raise UserError(_("The 'MSME Notify Before' value must be greater than 0. Please configure it in Settings."))

        documents = self.search([('expiry_date', '!=', False)])

        for document in documents:
            notification_date = document.expiry_date - timedelta(days=notify_before)

            if date_now == notification_date:
                users = document.owner_id
                if not users:
                    raise UserError(_("No users found to notify for document %s.") % document.name)

                template_id = self.env.ref('ajw_custom_documents.notify_document_expire_email').id
                template = self.env['mail.template'].browse(template_id)

                for user in users:
                    try:
                        template.with_context(email_to=user.email).send_mail(
                            document.id,
                            email_values={
                                'author_id': self.env.user.partner_id.id,
                                'email_to': user.email
                            },
                            force_send=True
                        )
                    except UserError as e:
                        raise UserError(_("Error while sending email to user %s: %s") % (user.name, str(e)))