from django.urls import path

from . import views

app_name = "area"
urlpatterns = [
    path("", views.get_area, name="area"),
    path("<int:area_id>/take/<int:user_id>", views.BuyAreaAPIView.as_view()),
    path("insert_demo", views.demo, name="insert_demo")
]