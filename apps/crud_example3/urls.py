from django.urls import path

from . import views


app_name = "crud_example3"

# Function-Based and Class-Based View implementations
# Only one implementation should be present for each view, comment out the other(s)
# permthing_list has three implementations, the other views have two
urlpatterns = [
    # URL paths for the Function-Based View implementation
    #
    path("", views.permthing_list_view, name="permthing_list"),
    path("<int:pk>/", views.permthing_detail_view, name="permthing_detail"),
    path("new/", views.permthing_create_view, name="permthing_create"),
    path("<int:pk>/update/", views.permthing_update_view, name="permthing_update"),
    path("<int:pk>/delete/", views.permthing_delete_view, name="permthing_delete"),
    #
    # URL paths for the Class-Based View implementation
    #
    # path("", views.PermThingListHtmxView.as_view(), name="permthing_list"),
    # path("<int:pk>/", views.PermThingDetailView.as_view(), name="permthing_detail"),
    # path("new/", views.PermThingCreateView.as_view(), name="permthing_create"),
    # path("<int:pk>/update/", views.PermThingUpdateView.as_view(), name="permthing_update"),
    # path("<int:pk>/delete/", views.PermThingDeleteView.as_view(), name="permthing_delete"),
    #
    #  URL path for the htmx pagination implementation of a CBV list
    #
    # path("", views.PermThingListView.as_view(), name="permthing_list"),
    #
    # Special URL used to change my user's permissions, for demo purposes
    path("setperms/<int:perm_level>/", views.permthing_set_perms_view, name="permthing_set_perms"),
]
