from django.urls import path

from rest_framework import routers

from . import views


app_name = "crud_example2"

urlpatterns = [
    #
    # URL paths for the Function-Based View implementation
    #
    path("", views.teamthing_list_view, name="teamthing_list"),
    path("<int:pk>/", views.teamthing_detail_view, name="teamthing_detail"),
    path("new/", views.teamthing_create_view, name="teamthing_create"),
    path("<int:pk>/update/", views.teamthing_update_view, name="teamthing_update"),
    path("<int:pk>/delete/", views.teamthing_delete_view, name="teamthing_delete"),
    #
    # URL paths for the Class-Based View implementation
    #
    # path("", views.TeamThingListView.as_view(), name="teamthing_list"),
    # path("<int:pk>/", views.TeamThingDetailView.as_view(), name="teamthing_detail"),
    # path("new/", views.TeamThingCreateView.as_view(), name="teamthing_create"),
    # path("<int:pk>/update/", views.TeamThingUpdateView.as_view(), name="teamthing_update"),
    # path("<int:pk>/delete/", views.TeamThingDeleteView.as_view(), name="teamthing_delete"),
    #
    #  URL path for the htmx pagination implementation of a CBV list
    #
    # path("", views.TeamThingListHtmxView.as_view(), name="teamthing_list"),
]


# drf config
router = routers.DefaultRouter()
router.register("api/teamthings", views.TeamThingViewSet)

urlpatterns += router.urls
