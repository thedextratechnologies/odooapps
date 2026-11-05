
{
    "name": "Contact Branch & Employee Management",
    "version": "19.0.1.1.0",
    "category": "Human Resources/Employees",
    "summary": "Manage company headquarters, branches and employee assignments",
    "description": """
        Manage customer and vendor headquarters, branch contacts,
        employee assignments and automatic synchronisation of
        important sales settings across branches.
        
        Developed by Dextra Technologies.
    """,
    "author": "Dextra Technologies",
    "website": "https://www.dextratechnologies.com/",
    "license": "LGPL-3",

    "depends": [
        "base",
        "contacts",
        "hr",
    ],

    "data": [
        "views/res_partner_views.xml",
        "views/res_partner_search.xml",
        "views/hr_employee_view.xml",
    ],

    "images": ['static/description/banner.gif'],
    "installable": True,
    "application": True,
}

