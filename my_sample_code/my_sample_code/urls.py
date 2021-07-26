from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from store.views import (ProductAPIViewSet,
                         UpdateProductEconomicDataAPIView,
                         CartAPIView,
                         OrderAPIView,
                         ReportAPIView,
                         )

router_v1 = DefaultRouter()

router_v1.register(r'api/v1/product', ProductAPIViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/update_product_economic_data/', UpdateProductEconomicDataAPIView.as_view(),
         name='update_product_economic_data'),
    path('api/v1/cart/', CartAPIView.as_view(), name='cart'),
    path('api/v1/order/', OrderAPIView.as_view(), name='order'),
    path('api/v1/report/', ReportAPIView.as_view(), name='proceeds'),
]

urlpatterns += router_v1.urls
