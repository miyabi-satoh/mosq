from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'units', views.UnitViewSet)
router.register(r'prints', views.PrintViewSet)
router.register(r'archives', views.ArchiveViewSet)

urlpatterns = [
    path('hello/', views.HelloView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
