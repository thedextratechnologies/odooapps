from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    gym_member_id = fields.Many2one(
        'gym.member',
        string='Gym Member'
    )