# from django.shortcuts import render
# from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status, views, viewsets
from .models import Unit, PrintHead
from .serializers import PrintSerializer, UnitSerializer


class PrintViewSet(viewsets.ModelViewSet):
    queryset = PrintHead.objects.all()
    serializer_class = PrintSerializer

    def create(self, request):
        print_serializer = PrintSerializer(data=request.data)

        if not print_serializer.is_valid():
            print(print_serializer.errors)
            return Response("error", status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        result = print_serializer.save()
        return Response(result)


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
