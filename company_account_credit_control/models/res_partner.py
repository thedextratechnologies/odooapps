from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    account_number = fields.Char(
        string="Account Number",
        copy=False,
        readonly=True,
        index=True,
    )

    _account_number_unique = models.Constraint(
        "UNIQUE(account_number)",
        "The Account Number must be unique.",
    )

    def _assign_account_number_if_eligible(self):
        """Assign a unique account number to eligible companies."""

        sequence = self.env["ir.sequence"].sudo()

        for partner in self.sudo():
            if (
                partner.is_company
                and partner.use_partner_credit_limit
                and not partner.account_number
            ):
                number = sequence.next_by_code(
                    "res.partner.account"
                )

                if number:
                    super(ResPartner, partner).write({
                        "account_number": number,
                    })

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        partners._assign_account_number_if_eligible()
        return partners

    def write(self, vals):
        result = super().write(vals)

        if (
            "use_partner_credit_limit" in vals
            or "is_company" in vals
        ):
            self._assign_account_number_if_eligible()

        return result
