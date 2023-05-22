from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('createasset/',views.create_asset, name='create_asset'),
    path('', views.home, name='home'),
    path('assetlist/',views.asset_list, name='asset_list'),
    path('assetdetail/<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('maintenancelist/<int:asset_id>/', views.maintenance_list, name='maintenance_list'),
    path('addmaintenance/<int:asset_id>/', views.add_maintenance, name='add_maintenance'),
    path('repairlist/<int:asset_id>/', views.repair_list, name='repair_list'),
    path('addrepair/<int:asset_id>/', views.add_repair, name='add_repair'),
    path('asset/delete/<int:asset_id>/', views.asset_delete, name='asset_delete'),
    path('search', views.get_queryset, name='search_result'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('asset/edit/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('statistics/', views.asset_statistics, name='asset_statistics'),
]