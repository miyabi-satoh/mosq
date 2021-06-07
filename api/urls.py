from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'units', views.UnitViewSet)
router.register(r'prints', views.PrintViewSet)

urlpatterns = [
    path('hello/', views.HelloView.as_view()),
    path('prints/<int:printhead_id>/printout/', views.print_out),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
