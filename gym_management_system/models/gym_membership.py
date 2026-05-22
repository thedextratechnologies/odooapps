from odoo import models, fields

class GymMembership(models.Model):
    _name = "gym.membership"
    _description = 'Membership Plan'

    name = fields.Char(string='Name',required=True)
    # duration = fields.Integer(string="Duration (Days)")
    price = fields.Float(string="Price")
    description = fields.Text(string="Description")
    member_id = fields.Many2one('gym.member')
    partner_id = fields.Many2one('res.partner')

    def action_create_invoice(self):
        self.ensure_one()

        partner = self.member_id.partner_id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_move_type': 'out_invoice',
                'default_partner_id': partner.id,
                'default_invoice_line_ids': [(0, 0, {
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.price,
                })]
            }
        }