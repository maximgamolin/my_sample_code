from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from store.views import (ProductAPIViewSet,
                         UpdateProductEconomicDataAPIView,
                         CartAPIView,
                         OrderAPIView,
                         ReportAPIView,
                         )

import debug_toolbar
from django.conf import settings

router = DefaultRouter()

router.register(r'api/product', ProductAPIViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/update_product_economic_data/', UpdateProductEconomicDataAPIView.as_view(),
         name='update_product_economic_data'),
    path('api/cart/', CartAPIView.as_view(), name='cart'),
    path('api/order/', OrderAPIView.as_view(), name='order'),
    path('api/report/', ReportAPIView.as_view(), name='proceeds'),

    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += router.urls
