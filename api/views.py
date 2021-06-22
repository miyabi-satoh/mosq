from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.http.response import FileResponse, JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .utils import print_contest_pdf
from .models import Archive, PrintType, Unit, PrintHead
from .serializers import ArchiveSerializer, PrintSerializer, PrintTypeSerializer, UnitSerializer


class PrintViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = PrintHead.objects.all()
    serializer_class = PrintSerializer


class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    pagination_class = None


class PrintTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrintType.objects.all()
    serializer_class = PrintTypeSerializer
    pagination_class = None


class ArchiveViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer


class HelloView(views.APIView):
    """
    APIサンプル
    """

    def get(self, request, format=None):
        return Response({"message": "Hello World!"})


@api_view()
def print_out(request, printhead_id):
    printhead = get_object_or_404(PrintHead, pk=printhead_id)
    file = print_contest_pdf(printhead)
    if not file:
        return None

    archive = Archive()
    archive.printhead = printhead
    archive.file = file
    archive.title = printhead.title
    if request.query_params.get('archive'):
        archive.save()

    return FileResponse(archive.file)


@ensure_csrf_cookie
def csrf_cookie(request):
    """
    CSRFトークンをクッキーにセットする
    """
    return JsonResponse({"detail": "CSRF cookie set"})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    ログイン処理
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"detail": "Invalid credentails"}, status=400)

    login(request, user)
    return JsonResponse({
        "id": user.id,
        "username": user.username
    })


@api_view()
def me(request):
    """
    ログイン中のユーザーを返す
    """
    user = request.user
    return JsonResponse({
        "id": user.id,
        "username": user.username
    })
