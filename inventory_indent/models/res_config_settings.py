from odoo import fields, models, api


class InventoryIndentResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_indent_email = fields.Boolean(
        string='Enable Email Notifications',
        config_parameter='inventory_indent.enable_indent_email'
    )

    enable_indent_sms = fields.Boolean(
        string='Enable SMS Notifications',
        config_parameter='inventory_indent.enable_indent_sms'
    )

    indent_manager_ids = fields.Many2many(
        'res.users',
        string='Indent Managers'
    )

    @api.model
    def get_values(self):

        res = super().get_values()

        param = self.env['ir.config_parameter'].sudo()

        manager_ids = param.get_param(
            'inventory_indent.indent_manager_ids',
            default=''
        )

        ids_list = []

        if manager_ids:
            ids_list = [int(x) for x in manager_ids.split(',') if x]

        res.update({
            'indent_manager_ids': [(6, 0, ids_list)],
        })

        return res

    def set_values(self):

        super().set_values()

        param = self.env['ir.config_parameter'].sudo()

        manager_ids = ','.join(
            map(str, self.indent_manager_ids.ids)
        )

        param.set_param(
            'inventory_indent.indent_manager_ids',
            manager_ids
        )