from odoo import api, fields, models
from odoo.exceptions import ValidationError


class InventoryIndent(models.Model):
    _name = 'inventory.indent'
    _description = 'Inventory Indent'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id desc'

    name = fields.Char(
        string='Indent Number',
        required=True,
        readonly=True,
        copy=False,
        default='New',
        tracking=True
    )

    date = fields.Date(
        string='Indent Date',
        default=fields.Date.context_today,
        tracking=True
    )

    requested_by = fields.Many2one(
        'res.users',
        string='Requested By',
        default=lambda self: self.env.user,
        tracking=True
    )

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        tracking=True
    )

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        required=True,
        tracking=True
    )

    location_id = fields.Many2one(
        'stock.location',
        string='Source Location',
        required=True,
        domain="[('usage','=','internal')]"
    )
    destination_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        required=True,
        domain="[('usage','=','internal')]"
    )

    line_ids = fields.One2many(
        'inventory.indent.line',
        'indent_id',
        string='Indent Lines'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default='draft', tracking=True)

    picking_id = fields.Many2one(
        'stock.picking',
        string='Internal Transfer',
        readonly=True
    )

    total_qty = fields.Float(
        string='Total Quantity',
        compute='_compute_total_qty',
        store=True
    )

    def action_approve(self):

        for rec in self:
            rec.state = 'approved'

            rec.send_indent_approved_notification()

            rec.create_internal_transfer()

    @api.depends('line_ids.quantity')
    def _compute_total_qty(self):
        for rec in self:
            rec.total_qty = sum(rec.line_ids.mapped('quantity'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'inventory.indent'
                ) or 'New'
        return super().create(vals_list)

    def action_submit(self):
        for rec in self:
            if not rec.line_ids:
                raise ValidationError('Please add products.')
            rec.state = 'submitted'

    def action_approve(self):
        for rec in self:
            rec.create_internal_transfer()
            rec.state = 'approved'

    def action_done(self):
        for rec in self:
            if rec.picking_id:
                rec.picking_id.action_confirm()
                rec.picking_id.action_assign()

                for move in rec.picking_id.move_ids:
                    move.quantity = move.product_uom_qty

                rec.picking_id.button_validate()

            rec.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_reset_draft(self):
        self.state = 'draft'

    def create_internal_transfer(self):

        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('warehouse_id', '=', self.warehouse_id.id)
        ], limit=1)

        if not picking_type:
            raise ValidationError(
                'No Internal Transfer Operation Type Found!'
            )

        picking = self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.destination_location_id.id,
            'origin': self.name,
        })

        for line in self.line_ids:
            self.env['stock.move'].create({
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.destination_location_id.id,
                'picking_id': picking.id,
            })

        self.picking_id = picking.id

    def send_indent_request_notification(self):

        config = self.env['ir.config_parameter'].sudo()

        enable_email = config.get_param(
            'inventory_indent.enable_indent_email'
        )

        enable_sms = config.get_param(
            'inventory_indent.enable_indent_sms'
        )

        manager_ids = config.get_param(
            'inventory_indent.indent_manager_ids'
        )

        if manager_ids:

            user_ids = [
                int(x)
                for x in manager_ids.split(',')
                if x
            ]

            users = self.env['res.users'].browse(user_ids)

            # EMAIL

            if enable_email:

                template = self.env.ref(
                    'inventory_indent.mail_template_indent_request'
                )

                for user in users:

                    if user.email:
                        template.send_mail(
                            self.id,
                            force_send=True,
                            email_values={
                                'email_to': user.email,
                            }
                        )

            # SMS

            if enable_sms:

                for user in users:

                    if user.partner_id.mobile:
                        self.env['sms.api'].send_sms(
                            numbers=[user.partner_id.mobile],
                            message=f'Indent {self.name} requires approval'
                        )

    def send_indent_approved_notification(self):

        config = self.env['ir.config_parameter'].sudo()

        enable_email = config.get_param(
            'inventory_indent.enable_indent_email'
        )

        enable_sms = config.get_param(
            'inventory_indent.enable_indent_sms'
        )

        # EMAIL

        if enable_email and self.create_uid.email:
            template = self.env.ref(
                'inventory_indent.mail_template_indent_approved'
            )

            template.send_mail(
                self.id,
                force_send=True,
                email_values={
                    'email_to': self.create_uid.email,
                }
            )

        # SMS

        if enable_sms and self.create_uid.partner_id.mobile:
            self.env['sms.api'].send_sms(
                numbers=[self.create_uid.partner_id.mobile],
                message=f'Indent {self.name} approved'
            )

