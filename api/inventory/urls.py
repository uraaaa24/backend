from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.inventory import views

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("products/", views.ProductView.as_view()),
    path("products/<int:id>/", views.ProductView.as_view()),
    path("purchases/", views.PurchaseView.as_view()),
    path("sales/", views.SalesView.as_view()),
    path("inventories/<int:id>/", views.InventoryView.as_view()),
]
