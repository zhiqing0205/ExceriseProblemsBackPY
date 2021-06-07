from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from one.models import *
import json
from django.core import serializers
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProblemSerializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly,AllowAny



@receiver(post_save, sender=settings.AUTH_USER_MODEL) #Django的信号机制
def generate_token(sender, instance=None, created=False, **kwargs):
    '''
    创建用户时自动生成Token
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    '''
    if created:
        Token.objects.create(user=instance)

"""一、函数式编程 Function Based View"""
@api_view(["GET", "POST"])
# @authentication_classes((BasicAuthentication,SessionAuthentication,TokenAuthentication))
# @permission_classes((IsAuthenticated,))
def problem_list(request):
    """
    获取所有题目信息或新增一个题目
    :param request:
    :return:
    """
    if request.method == "GET":
        s = ProblemSerializers(instance=Problem.objects.all() ,many=True)
        return Response(s.data , status=status.HTTP_200_OK)

    elif request.method == "POST":
        s = ProblemSerializers(data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
# @authentication_classes((BasicAuthentication,SessionAuthentication,TokenAuthentication))
# @permission_classes((IsAuthenticated,))
def problem_type(request):
    """
    获取所有题目信息或新增一个题目
    :param request:
    :return:
    """
    type = request.GET.get('type')
    if request.method == "GET":
        s = ProblemSerializers(instance=Problem.objects.filter(type=type) ,many=True)
        return Response(s.data , status=status.HTTP_200_OK)


@api_view(["GET" , "PUT" , "DELETE"])
def problem_detail(request , id):
    """
    获取、更新、删除一个课程
    :param request:
    :param id:
    :return:
    """
    try:
        problem = Problem.objects.get(id=id)
    except Problem.DoesNotExist:
        return Response(data={"msg": "没有该题目信息"} , status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        s = ProblemSerializers(instance=problem)
        return  Response(data=s.data , status = status.HTTP_200_OK)

    elif request.method == "PUT":
        s = ProblemSerializers(instance=problem , data=request.data)
        if s.is_valid():
            s.save()
            return  Response(data=s.data , status=status.HTTP_200_OK)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        problem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProblemList(APIView):

    authentication_classes=(BasicAuthentication,SessionAuthentication,TokenAuthentication)

    permission_classes = (IsAuthenticated,)

    def get(self , request):
        """
        :param request:
        :return:
        """
        queryset = Problem.objects.all()
        s = ProblemSerializers(instance=queryset, many=True)    #这里instance 后端数据
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self , request):
        """
        :param request:
        :return:
        """
        s = ProblemSerializers(data=request.data)       # 这里的data 是前端传递的 return前需要校验
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class ProblemDetail(APIView):

    @staticmethod
    def get_object(id):
        try:
            return Problem.objects.get(id=id)
        except Problem.DoesNotExist:
            return

    def get(self , request , id):
        '''
        :param request:
        :param id:
        :return:
        '''
        obj = self.get_object(id)
        if not obj:
            return Response(data={"msg": "没有该题目信息"}, status=status.HTTP_404_NOT_FOUND)
        s = ProblemSerializers(instance=obj)
        return Response(data=s.data, status=status.HTTP_200_OK)

    def put(self , request , id):
        obj = self.get_object(id)
        if not obj:
            return Response(data={"msg": "没有该题目信息"}, status=status.HTTP_404_NOT_FOUND)
        s = ProblemSerializers(instance=obj , data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_200_OK)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , id):
        obj = self.get_object(id)
        if not obj:
            return Response(data={"msg": "没有该题目信息"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



"""三、通用类视图  Generic Class Based View"""
class GProblemList(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializers

class GProblemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializers


"""四、DRF的视图集viewsets"""
class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializers