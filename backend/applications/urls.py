from django.urls import path
from .views import ApplicationListCreateView, ApplicationDetailView, dashboard_stats

urlpatterns = [
    path('', ApplicationListCreateView.as_view()),
    path('<int:pk>/', ApplicationDetailView.as_view()),
    path('dashboard/stats/', dashboard_stats),
]
