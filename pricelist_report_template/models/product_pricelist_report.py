from odoo import http
from odoo.http import request
import base64

class PricelistStoreController(http.Controller):

    @http.route('/pricelist/store_pdf', type='http', auth='user')
    def store_pdf(self, pricelist_id=None, **kw):
        """Generate PDF, store in Documents, and download."""

        if not pricelist_id:
            return request.not_found()

        pricelist = request.env['product.pricelist'].sudo().browse(int(pricelist_id))

        report = request.env.ref('product.action_report_pricelist')
        pdf, _ = report._render_qweb_pdf([pricelist.id])

        attachment = request.env['ir.attachment'].sudo().create({
            'name': f"{pricelist.name}.pdf",
            'type': 'binary',
            'datas': base64.b64encode(pdf),
            'res_model': 'product.pricelist',
            'res_id': pricelist.id,
            'mimetype': 'application/pdf',
        })

        # Store in Documents root
        request.env['documents.document'].sudo().create({
            'name': attachment.name,
            'attachment_id': attachment.id,
        })

        return request.make_response(
            pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', f'attachment; filename="{pricelist.name}.pdf"'),
            ],
        )