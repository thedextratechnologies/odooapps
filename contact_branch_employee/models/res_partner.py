from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------

    is_headquarter = fields.Boolean(
        string="Is Headquarter",
        default=False,
    )

    is_branch = fields.Boolean(
        string="Branch",
        compute="_compute_is_branch",
        store=True,
    )

    headquarter_id = fields.Many2one(
        "res.partner",
        string="Headquarter",
        domain="[('is_headquarter','=',True)]",
        ondelete="restrict",
        index=True,
    )

    branch_ids = fields.One2many(
        "res.partner",
        "headquarter_id",
        string="Branches",
    )

    branch_count = fields.Integer(
        string="Branch Count",
        compute="_compute_branch_count",
    )

    # -------------------------------------------------------------------------
    # Compute
    # -------------------------------------------------------------------------

    @api.depends("headquarter_id")
    def _compute_is_branch(self):
        for rec in self:
            rec.is_branch = bool(rec.headquarter_id)

    @api.depends("branch_ids")
    def _compute_branch_count(self):
        for rec in self:
            rec.branch_count = len(rec.branch_ids)

    # -------------------------------------------------------------------------
    # Create
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("is_headquarter"):
                vals["headquarter_id"] = False

        return super().create(vals_list)

    # -------------------------------------------------------------------------
    # Write
    # -------------------------------------------------------------------------

    def write(self, vals):
        vals = vals.copy()

        # A Headquarter cannot belong to another Headquarter
        if vals.get("is_headquarter"):
            vals["headquarter_id"] = False

        # Save record first
        res = super().write(vals)

        # Avoid recursive updates
        if self.env.context.get("skip_branch_sync"):
            return res

        # Fields that should sync from HQ -> Branches
        sync_fields = [
            "user_id",
            "property_product_pricelist",
            "property_payment_term_id",
            "property_inbound_payment_method_line_id",
        ]

        sync_vals = {
            field: vals[field]
            for field in sync_fields
            if field in vals
        }

        if not sync_vals:
            return res

        for partner in self:

            # ---------------------------------------------------------
            # HEADQUARTER UPDATED
            # Sync to all branches
            # ---------------------------------------------------------
            if partner.is_headquarter:

                if partner.branch_ids:
                    partner.branch_ids.with_context(
                        skip_branch_sync=True
                    ).write(sync_vals)

            # ---------------------------------------------------------
            # BRANCH UPDATED
            # Do nothing.
            # Only this branch is updated.
            # No synchronization to HQ or other branches.
            # ---------------------------------------------------------
            elif partner.is_branch:
                pass

        return res

    # -------------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------------

    @api.constrains("is_headquarter", "headquarter_id")
    def _check_headquarter_branch(self):
        for partner in self:

            # HQ cannot belong to another HQ
            if partner.is_headquarter and partner.headquarter_id:
                raise ValidationError(
                    _("A Headquarter cannot belong to another Headquarter.")
                )

            # Prevent self-reference
            if partner.headquarter_id == partner:
                raise ValidationError(
                    _("A contact cannot be its own Headquarter.")
                )

    # -------------------------------------------------------------------------
    # Onchange
    # -------------------------------------------------------------------------

    @api.onchange("is_headquarter")
    def _onchange_is_headquarter(self):
        if self.is_headquarter:
            self.headquarter_id = False

    @api.onchange("headquarter_id")
    def _onchange_headquarter(self):
        if self.headquarter_id:
            self.is_headquarter = False

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def action_open_full_form(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Contact"),
            "res_model": "res.partner",
            "view_mode": "form",
            "res_id": self.id,
            "target": "current",
        }