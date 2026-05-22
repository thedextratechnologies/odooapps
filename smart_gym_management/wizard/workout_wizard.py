from odoo import models, fields
from odoo.http import request
from markupsafe import Markup
import urllib.parse


class GymWorkoutAssignWizard(models.TransientModel):
    _name = 'gym.workout.assign.wizard'
    _description = 'Workout Assign Wizard'

    member_id = fields.Many2one('gym.member', string="Member")
    trainer_id = fields.Many2one('gym.trainer', string="Trainer")

    exercise_id = fields.Many2one(
        'gym.exercise',
        string="Exercise"
    )

    duration = fields.Integer(string="Duration")
    description = fields.Html(string="Description")

    def action_send_whatsapp(self):

        description_text = self.description or ''

        message = f"""
🏋️ Workout Assigned

👤 Member: {self.member_id.name}
🏋️ Trainer: {self.trainer_id.name}
💪 Exercise: {self.exercise_id.name}
⏱ Duration: {self.duration} mins

📝 Description:
{description_text}
"""

        phone = self.member_id.phone or ''

        whatsapp_url = (
            "https://wa.me/%s?text=%s"
            % (phone, urllib.parse.quote(message))
        )

        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }

    def action_send_sms(self):

        description_text = self.description or ''

        message = f"""
Workout Assigned

Member: {self.member_id.name}
Trainer: {self.trainer_id.name}
Exercise: {self.exercise_id.name}
Duration: {self.duration} mins

Description:
{description_text}
"""

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'SMS',
                'message': message,
                'sticky': False,
            }
        }