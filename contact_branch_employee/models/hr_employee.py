from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    contact_id = fields.Many2one(
        "res.partner",
        string="Customer / Vendor Contact",
        domain=[
            "|",
            ("customer_rank", ">", 0),
            ("supplier_rank", ">", 0),
        ],
    )

    assignment_type = fields.Selection(
        [
            ("hq", "Headquarter"),
            ("branch", "Branch"),
        ],
        string="Assignment Type",
        default="hq",
        required=True,
    )

    headquarter_id = fields.Many2one(
        "res.partner",
        string="Headquarter",
        domain="[('is_headquarter', '=', True)]",
        tracking=True,
    )

    branch_id = fields.Many2one(
        "res.partner",
        string="Branch",
        domain="""
            [
                ('is_branch','=',True),
                ('headquarter_id','=',headquarter_id)
            ]
        """,
    )

    company_partner_id = fields.Many2one(
        "res.partner",
        string="Assigned Company",
        compute="_compute_company_partner",
        store=True,
    )

    @api.depends("assignment_type", "headquarter_id", "branch_id")
    def _compute_company_partner(self):
        for employee in self:
            if employee.assignment_type == "hq":
                employee.company_partner_id = employee.headquarter_id
            else:
                employee.company_partner_id = employee.branch_id

    @api.onchange("assignment_type")
    def _onchange_assignment_type(self):
        if self.assignment_type == "hq":
            self.branch_id = False
        else:
            self.headquarter_id = False

    @api.onchange("headquarter_id")
    def _onchange_headquarter(self):

        self.branch_id = False

    @api.constrains("assignment_type", "headquarter_id", "branch_id")
    def _check_assignment(self):
        for employee in self:

            if employee.assignment_type == "hq":
                if not employee.headquarter_id:
                    raise ValidationError(
                        _("Please select a Headquarter.")
                    )

                if employee.branch_id:
                    raise ValidationError(
                        _("An employee assigned to a Headquarter cannot have a Branch.")
                    )

            if employee.assignment_type == "branch":
                if not employee.headquarter_id:
                    raise ValidationError(
                        _("Please select the Headquarter first.")
                    )

                if not employee.branch_id:
                    raise ValidationError(
                        _("Please select a Branch.")
                    )

                if employee.branch_id.headquarter_id != employee.headquarter_id:
                    raise ValidationError(
                        _("The selected Branch does not belong to the selected Headquarter.")
                    )

    def write(self, vals):
        for employee in self:
            # Prevent Branch Salesperson from changing Headquarter
            if (
                    employee.assignment_type == "branch"
                    and "headquarter_id" in vals
                    and employee.headquarter_id
                    and vals["headquarter_id"] != employee.headquarter_id.id
            ):
                raise ValidationError(
                    _("Branch Salespersons are not allowed to change the assigned Headquarter.")
                )

        return super().write(vals)