import json
from odoo import models, fields

class VariantSelectionWizard(models.TransientModel):
    _name = 'variant.selection.wizard'
    _description = 'Variant Selection Wizard'

    pricelist_id = fields.Many2one('product.pricelist', string="Pricelist")

    product_ids = fields.Many2many('product.product', string="Products")

    quantity_ids = fields.Char(default="1")

    pricelist_name = fields.Char()
    customer_name = fields.Char()
    document_no = fields.Char()

    # ✅ PREVIEW
    def action_preview(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_url',
            'url': '/report/html/pricelist_variant_report.report_variant_pricelist/%s?context=%s'
                   % (self.pricelist_id.id, json.dumps({'wizard_id': self.id})),
            'target': 'new',
        }

    # ✅ PDF DOWNLOAD (FIXED)
    def action_print_pdf(self):
        self.ensure_one()

        return self.env.ref(
            'pricelist_variant_report.report_pricelist_product_variant'
        ).report_action(
            self.pricelist_id,
            data={'wizard_id': self.id}   # ✅ IMPORTANT
        )