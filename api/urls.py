from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'master/units', views.UnitViewSet)
router.register(r'master/printtypes', views.PrintTypeViewSet)
router.register(r'prints', views.PrintViewSet)
router.register(r'archives', views.ArchiveViewSet)

urlpatterns = [
    path('hello/', views.HelloView.as_view()),
    path('csrf-cookie/', views.csrf_cookie),
    path('login/', views.login_view),
    path('users/me/', views.me)
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
