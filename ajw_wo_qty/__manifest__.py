{
    'name': 'WO Qty Tracking',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'depends': ['mrp', 'mrp_workorder'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'ajw_wo_qty/static/src/mrp_display_patch.xml',
            ('append', 'ajw_wo_qty/static/src/mrp_display_action_patch.js'),
            ('append', 'ajw_wo_qty/static/src/mrp_register_dialog_patch.js'),
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}