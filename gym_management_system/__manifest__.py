{
    'name': 'Gym Management',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Comprehensive gym management system to manage members, trainers, memberships, workouts and billing operations efficiently. Helps streamline daily gym activities with modern tracking and reporting features.',
    'depends': ['base', 'product', 'account'],
    'author' : 'Dextra Technologies',
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/dashboard_menu.xml',
        'views/gym_member_views.xml',
        'views/gym_membership_views.xml',
        'views/gym_trainer_views.xml',
        'views/gym_workout_views.xml',
        'views/gym_product_action.xml',
        'views/gym_product_views.xml',
        'views/gym_exercise_views.xml',
        'views/gym_payment_report.xml',
        'wizard/workout_wizard.xml',

    ],

    'assets': {
        'web.assets_backend': [
            'gym_management_system/static/src/js/dashboard.js',
            'gym_management_system/static/src/xml/dashboard.xml',
            'gym_management_system/static/src/css/dashboard.css',

            # Chart JS CDN
            'https://cdn.jsdelivr.net/npm/chart.js',
        ],
    },
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
}
