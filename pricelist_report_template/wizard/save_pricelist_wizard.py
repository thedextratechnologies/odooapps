from odoo import models, fields


class SavePricelistWizard(models.TransientModel):
    _name = "save.pricelist.wizard"
    _description = "Save Pricelist Wizard"

    pricelist_id = fields.Many2one("product.pricelist", required=True)

    print_type = fields.Selection(
        [
            ("with_variants", "With Variants"),
            ("without_variants", "Without Variants"),
        ],
        default="with_variants",
        required=True,
    )

    def action_confirm(self):
        if self.print_type == "with_variants":
            return self.pricelist_id.action_print_with_variants()
        return self.pricelist_id.action_print_without_variants()
