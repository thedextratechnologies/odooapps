{
    'name': 'Pricelist Variant Report',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Generate professional variant-based pricelist reports with preview and PDF export',

    'description': """ Select product variants from pricelist and generate report""",

    'author': 'Dextra Technologies',
    'website': 'https://www.dextratechnologies.com',

    'license': 'OPL-1',

    'depends': [
        'product',
        'sale',
],

    'data': [
        'security/ir.model.access.csv',
        'views/pricelist_view.xml',
        'wizard/wizard_view.xml',
        'report/report_template.xml',
    ],

    'images': [
        'static/description/banner.gif',
    ],

    'price': 25.00,
    'currency': 'USD',

    'installable': True,
    'application': False,
}