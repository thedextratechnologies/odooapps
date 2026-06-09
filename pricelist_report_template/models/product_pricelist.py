from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"


    # For Pricelists Level Field Definition while PDF Report Generation
    pricelist_name = fields.Char("Pricelist Name")
    document_no = fields.Char("Document No")
    customer_name = fields.Char("Customer Name")
    confidential_note = fields.Text("Confidential Note")

    def action_print_pricelist(self):
        """Open confirmation wizard instead of direct print"""
        return {
            "type": "ir.actions.act_window",
            "res_model": "save.pricelist.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_pricelist_id": self.id,
            },
        }




