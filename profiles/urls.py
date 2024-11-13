from django.urls import path
from.import views

urlpatterns = [
    path('profile/',views.profileView, name='employee'),
    path('create_review/',views.create_review, name='createreview'),
    path('employer-update/',views.employerProfileUpdateView, name='employerupdate'),
    path('housemanager-update/',views.houseManagerProfileUpdateView, name='housemanagerupdate'),
    path('search/',views.searchView, name='searchView'),
    path('house-managers/<int:id>',views.house_manager_detail_view, name='houseManagersDetailView'),
    path('employer/<int:id>',views.employer_detail_view, name='employerDetailDetailView'),
]