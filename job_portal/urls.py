
from django.urls import path, include
from job_portal import views

urlpatterns = [
    path('',views.index,name='index'),
    path('job_listing/',views.job_list,name='joblist'),
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/', views.logout_user, name='logout'),
    #path('apply/', views.apply, name='apply'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('job/search/', views.job_search, name='job_search'),
    path('create_job', views.create_job, name='create_job'),
    path('edit_job/<int:job_id>',views.edit_job,name='edit_job'),
    path('delete_job/<int:job_id>',views.delete_job,name='delete_job'),
    path('calculate_salary/',views.calculate_salary,name='calculate_salary'),

]
