from django.urls import path

from . import views


app_name = "crud_example4"

# Function-Based and Class-Based View implementations
# Only one implementation should be present for each view, comment out the other(s)
# inputthing_list has three implementations, the other views have two
urlpatterns = [
    # We're only offering Class-Based Views, and HTMX paging
    #
    path("", views.InputThingListHtmxView.as_view(), name="inputthing_list"),
    path("<int:pk>/", views.InputThingDetailView.as_view(), name="inputthing_detail"),
    path("new/", views.InputThingCreateView.as_view(), name="inputthing_create"),
    path("<int:pk>/update/", views.InputThingUpdateView.as_view(), name="inputthing_update"),
    path("<int:pk>/delete/", views.InputThingDeleteView.as_view(), name="inputthing_delete"),
]
