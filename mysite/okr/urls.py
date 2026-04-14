from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/<int:pk>/', views.dashboard, name='dashboard'),
    path('<int:year>/<int:month>/<int:kr_id>/', views.action_items, name='action_items'),
    path('key-result/new/<int:objective_pk>/', views.month_result_calc, name='key_result_create'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('signup/', views.register, name='signup'),
    path('action/delete/<int:pk>/', views.action_delete, name='action_delete'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]

