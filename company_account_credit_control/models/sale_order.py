from collections import defaultdict

from odoo import fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        grouped_orders = defaultdict(lambda: self.browse())

        for order in self:
            if order.state not in ("draft", "sent"):
                continue

            partner = order.partner_id.commercial_partner_id
            grouped_orders[(partner.id, order.company_id.id)] |= order

        for orders in grouped_orders.values():
            first_order = orders[0]

            partner = first_order.partner_id.commercial_partner_id.with_company(
                first_order.company_id
            )

            if not partner.use_partner_credit_limit:
                continue

            credit_limit = partner.credit_limit

            if not credit_limit:
                continue

            company = first_order.company_id
            company_currency = company.currency_id

            current_orders_amount = 0.0

            for order in orders:
                current_orders_amount += order.currency_id._convert(
                    order.amount_total,
                    company_currency,
                    company,
                    order.date_order.date()
                    if order.date_order
                    else fields.Date.today(),
                )

            outstanding = partner.credit
            pending_orders = partner.credit_to_invoice

            total_credit = (
                outstanding
                + pending_orders
                + current_orders_amount
            )

            if company_currency.compare_amounts(
                total_credit, credit_limit
            ) > 0:
                raise UserError(_(
                    "Sales Order Confirmation Blocked: the customer's credit "
                    "limit would be exceeded.\n\n",
                    customer=partner.display_name,
                    limit=company_currency.format(credit_limit),
                    outstanding=company_currency.format(outstanding),
                    pending=company_currency.format(pending_orders),
                    current=company_currency.format(current_orders_amount),
                    total=company_currency.format(total_credit),
                ))

        return super().action_confirm()

