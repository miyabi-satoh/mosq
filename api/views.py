# from django.shortcuts import render
# from django.db.models import Count
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Unit, PrintHead
from .serializers import PrintSerializer, UnitSerializer


class PrintViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = PrintHead.objects.all()
    serializer_class = PrintSerializer


class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [AllowAny]
    # queryset = Unit.objects.annotate(
    #     question_count=Count('question')
    # ).filter(question_count__gt=0)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class HelloView(views.APIView):
    """
    APIサンプル
    """

    def get(self, request, format=None):
        return Response({"message": "Hello World!"})
