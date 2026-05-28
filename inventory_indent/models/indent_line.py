from odoo import fields, models


class InventoryIndentLine(models.Model):
    _name = 'inventory.indent.line'
    _description = 'Inventory Indent Line'

    indent_id = fields.Many2one(
        'inventory.indent',
        string='Indent Reference',
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )

    description = fields.Char(
        string='Description'
    )

    quantity = fields.Float(
        string='Quantity',
        default=1
    )

    approved_qty = fields.Float(
        string='Approved Quantity'
    )

    uom_id = fields.Many2one(
        'uom.uom',
        string='UOM',
        related='product_id.uom_id',
        store=True
    )

    available_qty = fields.Float(
        string='Available Qty',
        related='product_id.qty_available'
    )