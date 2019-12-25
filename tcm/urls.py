from django.urls import path

from tcm.views import (
    TcmView, LiteratureView, HandianProductView,
    PrescriptionView, XingWeiView, SearchView,
    TermView,
)

urlpatterns = [
    path('term/', TermView.as_view({'get': 'list'}), name='term-list'),

    path('term/<int:neo_id>/', TermView.as_view({'get': 'retrieve'}), name='term-detail'),

    path('tcm/', TcmView.as_view({'get': 'list'}), name='tcm-list'),

    path('tcm/<int:neo_id>/', TcmView.as_view({'get': 'retrieve'}), name='tcm-detail'),

    path('literature/', LiteratureView.as_view({'get': 'list'}), name='literature-list'),

    path('literature/<int:neo_id>/', LiteratureView.as_view({'get': 'retrieve'}), name='literature-detail'),

    path('product/', HandianProductView.as_view({'get': 'list'}), name='product-list'),

    # product详情:返回所有的关联节点
    path('product/<int:neo_id>/', HandianProductView.as_view({'get': 'retrieve'}), name='product-detail'),

    # product详情:关联节点根据页码返回
    path('product/<int:neo_id>/<int:page>/', HandianProductView.as_view({'get': 'retrieve'}), name='product-page-detail'),

    path('product/<int:neo_id>/relationship/<str:relationship>/', HandianProductView.as_view({'get': 'retrieve_relationship'}), name='product-relationship-detail'),

    path('product/<int:neo_id>/relationships/', HandianProductView.as_view({'get': 'relationships'}), name='product-relationship-list'),

    path('product/<int:neo_id>/literatures/', HandianProductView.as_view({'get': 'literatures'}), name='product-literature-list'),

    path('prescription/', PrescriptionView.as_view({'get': 'list'}), name='prescription-list'),

    path('prescription/<int:neo_id>/', PrescriptionView.as_view({'get': 'retrieve'}), name='prescription-detail'),

    path('xingwei/', XingWeiView.as_view({'get': 'list'}), name='xingwei-list'),

    path('xingwei/<int:neo_id>/', XingWeiView.as_view({'get': 'retrieve'}), name='xingwei-detail'),

    path('search/about/<str:info>/<str:search>/', SearchView.as_view({'get': 'get_about'}), name='search-about-list'),

    path('search/literature/<str:search>/', SearchView.as_view({'get': 'get_literature'}), name='search-literature-detail'),

    path('search/term/<str:search>/', SearchView.as_view({'get': 'get_term'}), name='search-term-detail'),

    path('search/prescription/<str:search>/', SearchView.as_view({'get': 'get_prescription'}), name='search-prescription-detail'),

    path('search/tcm/<str:search>/', SearchView.as_view({'get': 'get_tcm'}), name='search-tcm-detail'),

    path('about/prescription/<str:search>/', SearchView.as_view({'get': 'about_prescription'}), name='search-prescription-about'),

    path('about/tcm/<str:search>/', SearchView.as_view({'get': 'about_tcm'}), name='search-tcm-about'),

    path('about/term/<str:search>/', SearchView.as_view({'get': 'about_term'}), name='search-term-about'),
]
