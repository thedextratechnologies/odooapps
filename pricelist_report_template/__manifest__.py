{
    'name': 'Pricelist Report Template',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Generate professional pricelist reports with HTML preview and PDF export',

    'description': """customer-ready pricelist reports directly from Odoo.""",

    'author': 'Dextra Technologies',
    'website': 'https://www.dextratechnologies.com',
    'license': 'OPL-1',

    'depends': [
        'sale',
        'product',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/pricelist_view.xml',
        'wizard/save_pricelist_wizard.xml',
        'reports/pricelist_report.xml',
    ],

    'images': [
        'static/description/banner.gif',
    ],

    'price': 25.00,
    'currency': 'USD',

    'installable': True,
    'application': False,
}