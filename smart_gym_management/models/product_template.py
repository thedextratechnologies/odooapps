from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_gym_equipment = fields.Boolean()
    equipment_usage_note = fields.Text(string="Usage Instructions")
    maintenance_required = fields.Boolean(string="Maintenance Required")
