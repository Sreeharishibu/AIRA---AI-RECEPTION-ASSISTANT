from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('queries/', views.query_list, name='query_list'),
    path('queries/add/', views.add_query, name='add_query'),
    path('queries/edit/<int:pk>/', views.edit_query, name='edit_query'),
    path('delete_query/<int:pk>/', views.delete_query, name='delete_query'),
    path("analytics/", views.analytics_view, name="analytics"),
    path("stt/", views.stt_view, name="stt_api"),
    
    path('userhome/', views.userhome_view, name='userhome'),
    path("announcements/", views.announcements_view, name="announcements"),
    path("placement/", views.placement_view, name="placement"),
    path("add-details/", views.add_details_view, name="add_details"),
    path("details/delete/<int:pk>/", views.delete_detail_image, name="delete_detail_image"),

    path("inventory/", views.inventory_view, name="inventory_view"),
    path("inventory/add/", views.add_inventory, name="add_inventory"),
    path("inventory/edit/<int:pk>/", views.edit_inventory, name="edit_inventory"),
    path("inventory/delete/<int:pk>/", views.delete_inventory, name="delete_inventory"),
    path("inventory/details/", views.inventory_details, name="inventory_details"),
]