# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    """
    APIサンプル
    """

    def get(self, request, format=None):
        return Response({"message": "Hello World!"})
