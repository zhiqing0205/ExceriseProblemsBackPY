from django import forms
from  rest_framework import serializers

from .models import Problem
from django.contrib.auth.models import User

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','describe','opA','opB','opC','opD','answer')

class ProblemSerializers(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField()

    class Meta:
        model = Problem     #和上面的form类似
        #exclude = ('id',)   #注意元组中只有一个元素不能写成("id")
        #fields = ('id','describe','opA','opB','opC','opD','answer')
        fields = ('id','describe','opA','opB','opC','opD','answer','selected')
    def get_selected(self, obj):
        return ""

# class ProblemSerializers(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Problem     #和上面的form类似
#         #exclude = ('id',)   #注意元组中只有一个元素不能写成("id")
#         #url是默认值 可在setting.py中设置URL_DIELD_NAME使得全局生效
#         fields = ('id','url','describe','opA','opB','opC','opD','answer')
#         #fields = '__all__'