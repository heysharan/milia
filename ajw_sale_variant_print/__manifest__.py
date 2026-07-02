{
    'name': 'Sale Variant Print Control',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'depends': ['sale_management', 'product'],
    'data': [
        'views/product_attribute_views.xml',
        'views/sale_order_views.xml',
        'report/sale_order_report.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}