{
    'name': 'See Products to produce MRP summary in sales',
    'depends': ['sale_stock', 'mrp'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'assets': { 
        'web.assets_backend': [
        ],
    },
}
