from odoo import models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    def action_open_variant_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Variant wise Reports',
            'res_model': 'variant.selection.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_pricelist_id': self.id
            }
        }