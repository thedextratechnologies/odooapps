{
    "name": "Company Account Number & Credit Control",
    "version": "19.0.1.0.1",
    "category": "Accounting/Sales",
    "summary": "Unique company account numbers and strict sales credit-limit validation",
    "description": '''
Automatically assigns unique account numbers to company partners and blocks
sales order confirmation when an enabled partner credit limit would be exceeded.
''',
    "license": "LGPL-3",
    "author": "Dextra Technologies",
    "website": "https://www.dextratechnologies.com",
    "depends": ["sale_management", "account"],
    "data": [
        "data/ir_sequence.xml",
        "views/res_partner_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    'images': ['static/description/banner.gif'],
    "installable": True,
    "application": True,
}
