{
    'name': 'User Access Export',
    'version': '18.0.1.0.5',
    'category': 'Tools',
    'summary': 'Export Users and Their Application Group Access',
    'description': """
This module allows you to export all users along with their assigned groups by application in Excel format.
Useful for auditing user roles and permissions.
    """,
    'author': 'Lawrence Lanzaderas',
    'website': 'https://lawrencelanzaderas-portfolio.netlify.app/',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'wizard/export_user_access_wizard_views.xml',
    ],
    'installable': True,
    'application': False,

    'images': [
        'static/description/banner.gif',
        'static/description/screenshot1.png',
        'static/description/screenshot2.png',
        'static/description/screenshot3.png',
        'static/description/screenshot4.png',
        # 'static/description/icon.png',
    ],
}
