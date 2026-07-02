/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { MrpRegisterProductionDialog } from "@mrp_workorder/mrp_display/dialog/mrp_register_production_dialog";

patch(MrpRegisterProductionDialog, {
    props: {
        ...MrpRegisterProductionDialog.props,
        activeWorkorderId: { optional: true, type: Number },
    }
});

patch(MrpRegisterProductionDialog.prototype, {
    async doActionAndClose(action, saveModel = true, reloadChecks = false) {
        this.state.disabled = true;
        if (saveModel) {
            await this.props.record.save();

            await this.props.record.model.orm.call(
                "mrp.production",
                "set_qty_producing",
                this.props.record.resIds
            );

            const freshData = await this.props.record.model.orm.read(
                "mrp.production",
                this.props.record.resIds,
                ["qty_producing"]
            );
            const freshQty = freshData[0]?.qty_producing || 0;

            console.log("=== AJW dialog doActionAndClose ===");
            console.log("freshQty:", freshQty);
            console.log("activeWorkorderId:", this.props.activeWorkorderId);

            if (this.props.activeWorkorderId) {
                await this.props.record.model.orm.call(
                    "mrp.workorder",
                    "update_wo_qty_done",
                    [[this.props.activeWorkorderId], freshQty]
                );
            }
        }
        await this.props.reload(this.props.record);
        this.props.close();
    }
});