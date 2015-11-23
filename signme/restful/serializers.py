from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from restful.models import Lecture, Sign
from django.contrib.contenttypes.models import ContentType

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class LectureSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lecture
        exclude = ('group', 'student_want_sign')

class ListLectureSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize all lectures from today and tomorrow, not
    yesterday
    """
    start_time = serializers.ReadOnlyField(source='get_normal_start_time')
    end_time = serializers.ReadOnlyField(source='get_normal_end_time')

    class Meta:
        model = Lecture
        fields = ( 'name', 'id', 'date', 'start_time', 'end_time', 'count_student_want_sign')

class SignSerializer(serializers.HyperlinkedModelSerializer):
    
    # sent always for same lecture
    # id = serializers.ReadOnlyField(source='lecture.id')
    #user_id = serializers.ReadOnlyField(source='student.id')
    user_name = serializers.ReadOnlyField(source='student.name')
    user_status = serializers.ReadOnlyField(source='status')
    user_id = serializers.ReadOnlyField(source='student.id')
    
    class Meta:
        model = Sign

        fields = ('user_name', 'user_id', 'user_status','id',)

class LectureDetail(serializers.ModelSerializer):

    students = SignSerializer(source='sign_set', many=True)
    
    class Meta:
        model = Lecture
        fields = ('students',)



class NewLectureSerializer(serializers.ModelSerializer):

    start = serializers.IntegerField(read_only=True)
    end = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lecture
        fields = ('name', 'date', 'start', 'end')
    #TODO update 

class SwipeSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField()
    class Meta:
        model = Sign
        fields = ('id', 'status',)

class MySignSerializer(serializers.HyperlinkedModelSerializer):
    
    # sent always for same lecture
    # id = serializers.ReadOnlyField(source='lecture.id')
    #user_id = serializers.ReadOnlyField(source='student.id')
    user_status = serializers.ReadOnlyField(source='status')
    lecture = serializers.ReadOnlyField(source='lecture.name')
    
    class Meta:
        model = Sign

        fields = ('lecture', 'user_status','id',)


class UserSignSerializer(serializers.ModelSerializer):
    """List all signs from all lectures which user has requested.
    Finished also.
    """
    signs = MySignSerializer(source='sign_set', many=True)
    class Meta: 
        model = get_user_model()
        fields  = ('signs',)

class SignPicSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('sign_pic',)

class TopSignerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('name', 'beer',)

class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()

class NameChangeSerializer(serializers.Serializer):
    name = serializers.CharField()

class PhotoUploadSerializer(serializers.Serializer):
    photo = serializers.ImageField(read_only=True)

class SignRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sign
        exclude = ('status',)

