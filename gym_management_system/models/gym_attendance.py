# models/gym_attendance.py

from odoo import models, fields, api

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    is_gym = fields.Boolean(default=True)

    def action_check_in(self):
        for rec in self:
            # Prevent multiple open attendances
            existing = self.search([
                ('employee_id', '=', rec.employee_id.id),
                ('check_out', '=', False)
            ], limit=1)

            if not existing:
                rec.check_in = fields.Datetime.now()
                rec.is_gym = True

    def action_check_out(self):
        for rec in self:
            if rec.check_in and not rec.check_out:
                rec.check_out = fields.Datetime.now()