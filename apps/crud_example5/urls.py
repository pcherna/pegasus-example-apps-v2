from django.urls import path

from rest_framework import routers

from . import views


app_name = "crud_example5"

# Function-Based and Class-Based View implementations
# Only one implementation should be present for each view, comment out the other(s)
# sortfilterthing_list has three implementations, the other views have two
urlpatterns = [
    #
    # URL paths for the Function-Based View implementation
    #
    # path("", views.sortfilterthing_list_view, name="sortfilterthing_list"),
    # path("<int:pk>/", views.sortfilterthing_detail_view, name="sortfilterthing_detail"),
    # path("new/", views.sortfilterthing_create_view, name="sortfilterthing_create"),
    # path("<int:pk>/update/", views.sortfilterthing_update_view, name="sortfilterthing_update"),
    # path("<int:pk>/delete/", views.sortfilterthing_delete_view, name="sortfilterthing_delete"),
    #
    # URL paths for the Class-Based View implementation
    #
    path("", views.SortFilterThingListHtmxView.as_view(), name="sortfilterthing_list"),
    path("<int:pk>/", views.SortFilterThingDetailView.as_view(), name="sortfilterthing_detail"),
    path("new/", views.SortFilterThingCreateView.as_view(), name="sortfilterthing_create"),
    path("<int:pk>/update/", views.SortFilterThingUpdateView.as_view(), name="sortfilterthing_update"),
    path("<int:pk>/delete/", views.SortFilterThingDeleteView.as_view(), name="sortfilterthing_delete"),
]


# drf config
router = routers.DefaultRouter()
router.register("api/sortfilterthings", views.SortFilterThingViewSet)

urlpatterns += router.urls
