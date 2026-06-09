from odoo import models


class PricelistVariantReport(models.AbstractModel):
    _name = 'report.pricelist_variant_report.report_variant_pricelist'
    _description = 'Pricelist Variant Report'

    def _get_report_values(self, docids, data=None):

        # -----------------------------
        # Pricelist
        # -----------------------------
        pricelist = False

        if docids:
            pricelist = self.env['product.pricelist'].browse(docids[0])

        wizard_id = False

        if data and data.get('wizard_id'):
            wizard_id = data.get('wizard_id')
        elif self.env.context.get('wizard_id'):
            wizard_id = self.env.context.get('wizard_id')

        wizard = self.env['variant.selection.wizard'].browse(wizard_id) if wizard_id else False

        if not pricelist and wizard:
            pricelist = wizard.pricelist_id

        if not pricelist:
            raise ValueError("No pricelist found")

        # -----------------------------
        # Quantities
        # -----------------------------
        qty_string = wizard.quantity_ids if wizard and wizard.quantity_ids else "1,5,10"

        quantities = [
            int(x.strip())
            for x in qty_string.split(",")
            if x.strip().isdigit()
        ]

        # -----------------------------
        # IMPORTANT FIX HERE
        # -----------------------------
        # Use selected PRODUCT VARIANTS only (NOT templates)
        product_records = wizard.product_ids

        products = []

        for product in product_records:

            price_dict = {}

            for qty in quantities:
                res = pricelist._compute_price_rule(product, qty)
                price_dict[qty] = res.get(product.id, (0, False))[0]

            attribute_values = product.product_template_attribute_value_ids.mapped(
                'product_attribute_value_id.name'
            )

            products.append({
                'id': product.id,
                'name': product.product_tmpl_id.name,
                'description': product.product_tmpl_id.description_sale,
                'uom': product.uom_id.name,
                'price': price_dict,
                'attribute_values': attribute_values,
            })

        return {
            'doc_ids': docids,
            'doc_model': 'product.pricelist',
            'docs': pricelist,
            'pricelist': pricelist,

            'pricelist_name': wizard.pricelist_name if wizard and wizard.pricelist_name else pricelist.name,
            'customer_name': wizard.customer_name if wizard else '',
            'document_no': wizard.document_no if wizard else '',

            'quantities': quantities,
            'products': products,
        }