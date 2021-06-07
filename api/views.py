# from django.shortcuts import render
# from django.db.models import Count
# from django.core.files import File
from api.utils import create_print
from django.shortcuts import get_object_or_404
from django.http.response import FileResponse
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from .models import Archive, Unit, PrintHead
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


@api_view()
def print_out(request, printhead_id):
    printhead = get_object_or_404(PrintHead, pk=printhead_id)
    file = create_print(printhead)
    if not file:
        return None

    archive = Archive()
    archive.file = file
    archive.title = printhead.title
    archive.save()

    return FileResponse(archive.file)
