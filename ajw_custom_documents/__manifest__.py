# -*- coding: utf-8 -*-
{
    'name': "ajw_custom_documents",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','documents','web','hr','l10n_in_withholding'],

    # always loaded
    'data': [
        'security/ir.model.access.xml',
        'views/email_template.xml',
        'views/cron_jobs.xml',
        'views/res_config_settings_views.xml',
        'data/documents_folder_data.xml',
        'views/res_partner_view.xml',
        'views/documents_view.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'ajw_custom_documents/static/src/views/search/documents_control_panel.js',
            'ajw_custom_documents/static/src/views/search/documents_control_panel.xml',

        ],
                }

}

