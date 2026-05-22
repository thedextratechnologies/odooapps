from odoo import models, fields, api
from odoo.exceptions import UserError


class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'

    # -------------------------
    # BASIC INFO
    # -------------------------

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email')

    # Address
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Char(string='Zip')
    country_id = fields.Many2one('res.country', string='Country')
    image_1920 = fields.Image(string="Member Image")

    member_history = fields.Html(string="Member History")

    # Personal Info
    age = fields.Integer(string='Age')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')

    member_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string="Member Status", default='active')

    # Gym Info
    membership_id = fields.Many2one('gym.membership', string='Membership Plan')
    trainer_id = fields.Many2one('gym.trainer', string='Trainer')

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    # Physical Details
    height = fields.Float(string="Height (cm)")
    weight = fields.Float(string="Weight (kg)")

    bmi = fields.Float(
        string="BMI",
        compute="_compute_bmi",
        store=True
    )



    # -------------------------
    # CUSTOMER (AUTO CREATE)
    # -------------------------

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        readonly=True
    )

    # -------------------------
    # ACCOUNTING
    # -------------------------

    invoice_ids = fields.One2many(
        'account.move',
        'gym_member_id',
        string='Invoices'
    )

    invoice_count = fields.Integer(
        string='Invoice Count',
        compute='_compute_invoice_count'
    )

    payment_count = fields.Integer(
        string='Payment Count',
        compute='_compute_payment_count'
    )

    # -------------------------
    # STATUS
    # -------------------------

    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
    ], default='draft', string='Status')

    # -------------------------
    # CREATE CUSTOMER AUTOMATICALLY
    # -------------------------

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            partner = self.env['res.partner'].create({
                'name': vals.get('name'),
                'phone': vals.get('phone'),
                'email': vals.get('email'),
                'customer_rank': 1,
            })

            vals['partner_id'] = partner.id

        return super().create(vals_list)

    # -------------------------
    # UPDATE CUSTOMER AUTOMATICALLY
    # -------------------------

    def write(self, vals):
        res = super().write(vals)

        for rec in self:
            if rec.partner_id:
                rec.partner_id.write({
                    'name': rec.name,
                    'phone': rec.phone,
                    'email': rec.email,
                })

        return res

    # -------------------------
    # COMPUTE METHODS
    # -------------------------

    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids)

    def _compute_payment_count(self):
        for rec in self:

            payments = self.env['account.payment'].search([
                ('partner_id', '=', rec.partner_id.id)
            ])

            rec.payment_count = len(payments)

    @api.depends('height', 'weight')
    def _compute_bmi(self):

        for rec in self:
            if rec.height and rec.weight:
                h = rec.height / 100
                rec.bmi = rec.weight / (h * h)
            else:
                rec.bmi = 0

    # -------------------------
    # CREATE INVOICE
    # -------------------------

    def action_create_invoice(self):
        self.ensure_one()

        if not self.membership_id:
            raise UserError("Please select a Membership Plan.")

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'gym_member_id': self.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': f'{self.name} - {self.membership_id.name}',
                'quantity': 1,
                'price_unit': self.membership_id.price,
            })]
        })

        self.state = 'invoiced'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
        }

    # -------------------------
    # VIEW INVOICES
    # -------------------------

    def action_view_invoice(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('gym_member_id', '=', self.id)],
        }

    # -------------------------
    # VIEW PAYMENTS
    # -------------------------

    def action_view_payments(self):
        self.ensure_one()

        payments = self.env['account.payment'].search([
            ('partner_id', '=', self.partner_id.id)
        ])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', payments.ids)],
        }

    # -------------------------
    # CHECK PAYMENT STATUS
    # -------------------------

    def action_check_payment(self):
        for rec in self:

            invoices = rec.invoice_ids.filtered(
                lambda x: x.payment_state == 'paid'
            )

            if invoices:
                rec.state = 'paid'
