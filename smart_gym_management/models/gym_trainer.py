from odoo import models, fields, api

class GymTrainer(models.Model):
    _name = 'gym.trainer'
    _description = 'Gym Trainer'

    name = fields.Char(required=True)
    phone = fields.Char()
    specialty = fields.Char()
    image_1920 = fields.Image(string="Trainer Image")

    member_ids = fields.One2many('gym.member', 'trainer_id')

    member_count = fields.Integer(compute="_compute_member_count")

    @api.depends('member_ids')
    def _compute_member_count(self):
        for rec in self:
            rec.member_count = len(rec.member_ids)