from odoo import models, fields


class GymExercise(models.Model):
    _name = 'gym.exercise'

    name = fields.Char(
        string="Workout Name",
        required=True
    )