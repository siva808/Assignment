from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'fields', FieldViewSet)

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/machine/historical-data/', historical_data, name='historical-data'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('machine-data/', MachineDataCreateView.as_view(), name='machine-data-create'),
    path('machine-data/all/', MachineDataListView.as_view(), name='machine-data-list'),
    path('machine-data/historical/<str:axis_name>/', MachineHistoricalDataView.as_view(), name='machine-historical-data'),
     path('', include(router.urls)),
]

urlpatterns += router.urls
