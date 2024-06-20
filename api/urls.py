from django.urls import path
from . import views
urlpatterns = [
    path("user/<str:pk>", views.get_user, name="get-user"),
    path("add-hostel/", views.add_hostel, name="add-hostel"),
    path("get-hostels/", views.get_hostels, name="get-hostels"),
    path("get-hostel/<str:pk>/", views.get_hostel, name="get-hostel"),
    path("access-hostel/", views.access_hostel, name="access-hostel"),
    path("get-blocks/<str:pk>/", views.get_blocks, name="get-blocks"),
    path("add-block/", views.add_block, name="add-block"),
    path("get-rooms/<str:pk>/", views.get_rooms, name="get-rooms"),
    path("get-block/<str:pk>/", views.get_block, name="get-block"),
    path("add-student/", views.add_student, name="add-student"),
    path("get-room/<str:pk>/", views.get_room, name="get-room"),
    path("get-students/<str:pk>/", views.get_students, name="get-students"),
    path("get-hostel-data/<str:pk>/", views.get_hostel_data, name="get-hostel-data"),
    path("get-block-data/<str:pk>/", views.get_block_data, name="get-block-data"),
    path("edit-hostel/<str:pk>/", views.edit_hostel, name="edit-hostel"),
    path("delete-hostel/<str:pk>/", views.delete_hostel, name="delete-hostel"),
]
