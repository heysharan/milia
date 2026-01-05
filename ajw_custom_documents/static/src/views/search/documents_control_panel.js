/** @odoo-module **/
import { DocumentsControlPanel } from "@documents/views/search/documents_control_panel";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

patch(DocumentsControlPanel.prototype, {
    setup() {
        super.setup();
        this.action = useService("action");
    },

    async onExpireDate() {
        if (this.targetRecords.length !== 1) {
            return;
        }

        await this.openDialogExpire(this.targetRecords[0].data.id);
    },

    async openDialogExpire(documentId) {
        return new Promise((resolve) => {
            this.action.doAction(
                {
                    name: _t("Update"),
                    type: "ir.actions.act_window",
                    res_model: "documents.document",
                    res_id: documentId,
                    views: [[false, "form"]],
                    target: "new",
                    context: {
                        active_id: documentId,
                        dialog_size: "medium",
                        form_view_ref: "ajw_custom_documents.view_document_form_expiry_date",
                    },
                },
                {
                    onClose: async () => {
                        resolve();
                    },
                }
            );
        });
    }
});