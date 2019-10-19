from django.urls import path

from .views import (
    table_members, list_members, thumbnail_members, detail_member, edit_member, update_member, add_member, create_member, restore_member,
    delete_member, filter_members, search_members, get_members_by_statuses, get_members_by_shepherds, list_deleted_members,
    list_ministries, add_ministries, create_ministry,
    list_shepherds, add_shepherd, create_shepherd
)

urlpatterns = [
    # UrlConf For Members
    path('list/', list_members, name="list_members"),
    path('table/', table_members, name="table_members"),
    path('thumbnail/', thumbnail_members, name="thumbnail_members"),
    path('detail/<int:pk>/', detail_member, name="detail_member"),
    path('edit/<int:pk>/', edit_member, name="edit_member"),
    path('update/<int:pk>/', update_member, name="update_member"),
    path('add/', add_member, name="add_member"),
    path('create/', create_member, name="create_member"),
    path('delete/<int:pk>/', delete_member, name="delete_member"),
    path('filter/', filter_members, name="filter_members"),
    path('list/search/', search_members, name="search_members"),
    path('list/<status>/', get_members_by_statuses, name="get_members_by_statuses"),
    path('list_by_shepherd/<shepherd>/', get_members_by_shepherds, name="get_members_by_shepherd"),
    path('deleted/list/', list_deleted_members, name="list_deleted_members"),
    path('restore/<int:pk>/', restore_member, name="restore_members"),


    # UrlConf For Ministries
    path('ministries/list/', list_ministries, name="list_ministries"),
    path('ministries/add/', add_ministries, name="add_ministry"),
    path('ministries/create/', create_ministry, name="create_ministry"),

    # UrlConf For Shepherds
    path('shepherds/list/', list_shepherds, name="list_shepherds"),
    path('shepherds/add/', add_shepherd, name="add_shepherd"),
    path('shepherds/create/', create_shepherd, name="create_shepherd"),
]