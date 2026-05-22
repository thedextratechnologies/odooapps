from odoo import models, fields

class Diet(models.Model):
    _name = 'gym.diet'
    _description = 'Gym Diet'

    member_id = fields.Many2one('gym.member')
    trainer_id = fields.Many2one('gym.trainer')
    plan_details = fields.Text()
