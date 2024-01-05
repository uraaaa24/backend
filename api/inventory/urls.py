from django.urls import path

from api.inventory import views

urlpatterns = [
    path("products/", views.ProductView.as_view()),
    path("products/<int:id>/", views.ProductView.as_view()),
    path(
        "products/model/", views.ProductView.as_view({"get": "list", "post": "create"})
    ),
    path("purchases/", views.PurchaseView.as_view()),
    path("sales/", views.SalesView.as_view()),
    path("inventory/<int:id>/", views.InventoryView.as_view()),
]
