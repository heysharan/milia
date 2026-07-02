/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { MrpDisplayAction } from "@mrp_workorder/mrp_display/mrp_display_action";
import { MrpDisplayRecord } from "@mrp_workorder/mrp_display/mrp_display_record";

console.log("=== AJW patch loading ===");

patch(MrpDisplayAction.prototype, {
    get fieldsStructure() {
        const result = super.fieldsStructure;
        if (result["mrp.workorder"]) {
            if (!result["mrp.workorder"].includes("wo_qty_done")) {
                result["mrp.workorder"].push("wo_qty_done");
            }
            if (!result["mrp.workorder"].includes("wo_qty_remaining")) {
                result["mrp.workorder"].push("wo_qty_remaining");
            }
        }
        return result;
    }
});

patch(MrpDisplayRecord.prototype, {
    registerProduction() {
        const workorderId = this.resModel === "mrp.workorder"
            ? this.record.id
            : false;
        if (!this.props.production.data.qty_producing) {
            this.props.production.update({
                qty_producing: this.props.production.data.product_qty
            });
        }
        const { _t } = odoo.loader.modules.get("@web/core/l10n/translation");
        const title = _t(
            "Register Production: %s",
            this.props.production.data.product_id[1]
        );
        const { MrpRegisterProductionDialog } = odoo.loader.modules.get(
            "@mrp_workorder/mrp_display/dialog/mrp_register_production_dialog"
        );
        const params = {
            body: "",
            record: this.props.production,
            reload: this.env.reload.bind(this),
            title,
            qtyToProduce: this.record.qty_remaining,
            activeWorkorderId: workorderId,
        };
        this.dialog.add(MrpRegisterProductionDialog, params);
    },

    async quickRegisterProduction() {
        const { production } = this.props;
        const workorderId = this.record.id;
        const isWorkorder = this.resModel === "mrp.workorder" && workorderId;

        if (this.productionComplete) {
            if (isWorkorder) {
                const qtyToSet = production.data.qty_producing
                    || production.data.product_qty;
                await production.model.orm.call(
                    "mrp.workorder",
                    "update_wo_qty_done",
                    [[workorderId], qtyToSet]
                );
            }
            return this.registerProduction();
        }

        const qtyToSet = production.data.product_qty;
        await production.update({ qty_producing: qtyToSet }, { save: true });
        await production.model.orm.call(
            "mrp.production",
            "set_qty_producing",
            production.resIds
        );

        if (isWorkorder) {
            const freshData = await production.model.orm.read(
                "mrp.production",
                production.resIds,
                ["qty_producing"]
            );
            const freshQty = freshData[0]?.qty_producing || qtyToSet;
            await production.model.orm.call(
                "mrp.workorder",
                "update_wo_qty_done",
                [[workorderId], freshQty]
            );
        }

        await this.env.reload(this.props.production);
    }
});