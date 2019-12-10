from django.urls import path

from tcm.views import TcmView, LiteratureView, HandianProductView, PrescriptionView, XingWeiView

urlpatterns = [
    path('tcm/', TcmView.as_view({'get': 'list'}), name='tcm-list'),

    path('tcm/<int:neo_id>/', TcmView.as_view({'get': 'retrieve'}), name='tcm-detail'),

    path('literature/', LiteratureView.as_view({'get': 'list'}), name='literature-list'),

    path('literature/<int:neo_id>/', LiteratureView.as_view({'get': 'retrieve'}), name='literature-detail'),

    path('product/', HandianProductView.as_view({'get': 'list'}), name='product-list'),

    path('product/<int:neo_id>/', HandianProductView.as_view({'get': 'retrieve'}), name='product-detail'),

    path('product/<int:neo_id>/relationship/<str:relationship>/', HandianProductView.as_view({'get': 'retrieve_relationship'}), name='product-relationship-detail'),

    path('product/<int:neo_id>/relationships/', HandianProductView.as_view({'get': 'relationships'}), name='product-relationship-list'),

    path('product/<int:neo_id>/literatures/', HandianProductView.as_view({'get': 'literatures'}), name='product-literature-list'),

    path('prescription/', PrescriptionView.as_view({'get': 'list'}), name='Prescription-list'),

    path('prescription/<int:neo_id>/', PrescriptionView.as_view({'get': 'retrieve'}), name='Prescription-detail'),

    path('xingwei/', XingWeiView.as_view({'get': 'list'}), name='XingWei-list'),

    path('xingwei/<int:neo_id>/', XingWeiView.as_view({'get': 'retrieve'}), name='XingWei-detail'),
]
