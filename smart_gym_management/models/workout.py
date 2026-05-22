from odoo import models, fields

class GymWorkout(models.Model):
    _name = 'gym.workout'
    _description = 'Gym Workout'

    exercise_id = fields.Many2one(
        'gym.exercise',
        string="Workout",
        required=True
    )

    member_id = fields.Many2one(
        'gym.member',
        string="Member",
        required=True
    )

    trainer_id = fields.Many2one(
        'gym.trainer',
        string="Trainer"
    )

    duration = fields.Integer(string="Duration (minutes)")

    description = fields.Html(string="Description")

    equipment_ids = fields.Many2many(
        'product.template',
        string="Equipments",
        domain=[('is_gym_equipment', '=', True)]
    )

    def action_open_assign_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assign Workout',
            'res_model': 'gym.workout.assign.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_member_id': self.member_id.id,
                'default_trainer_id': self.trainer_id.id,
                'default_exercise_id': self.exercise_id.id,
                'default_duration': self.duration,
                'default_description': self.description,
            }
        }