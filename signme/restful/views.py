from re import match

from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import render
from restful.models import Student, Lecture, Sign
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from restful.serializers import SignRequestSerializer, UserSerializer, LectureSerializer, NewLectureSerializer, ListLectureSerializer, LectureDetail, SwipeSerializer, UserSignSerializer, SignPicSerializer, TopSignerSerializer, PasswordChangeSerializer, NameChangeSerializer, PhotoUploadSerializer
from django.contrib.auth.models import Group
from django.core import serializers
from rest_framework.views import APIView

from time import strptime, mktime
from datetime import date, timedelta, datetime
from django.utils import timezone
from django.db.models import Q
from push_notifications.models import GCMDevice
import pytz

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = UserSerializer

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    return render(request, 'index.html')

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def lecture_list(request):
    """
    List all lectures
    """
    if request.method == 'GET':
        # request.user.groups.all() always return only one group
        try: 
            group = request.user.groups.all()[0]
        except Exception:
            return JSONResponse({'status':110}, status=400)
        
        startdate = date.today()
        enddate = date.today() + timedelta(4)
        try:
            lectures = Lecture.objects.filter(Q(group=group)&Q(date__range=[startdate, enddate]))
        except:
            return JSONResponse({'status':110}, status=400)
        serializer = ListLectureSerializer(lectures, many=True)
        #serializer = ListLectureSerializer(context={'request':request}, many=True)
        data = {"lectures": serializer.data}
        return JSONResponse(data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NewLectureSerializer(data=data)
        """
        #TODO
        if data['today'] is True:
            midnight = timezone.now().replace(hour=0, minute=0, second=0)
            mydate = timezone.now().date().isoformat()
        else:
            mydate = timezone.now() + timedelta(days=1)
            midnight = mydate.replace(hour=0, minute=0, second=0)
            mydate = mydate.date()
        """
        _date = datetime.fromtimestamp(mktime(strptime(data['date'], "%Y-%m-%d")))
        midnight = _date.replace(hour=0, minute=0, second=0)
        # TODO: if application expands make timezone aware
        start_hour = midnight + timedelta(hours=data['start']+2)
        end_hour = midnight + timedelta(hours=data['end']+2)
        _date = _date.date()
        if serializer.is_valid():
            serializer.save(date=_date, start_hour=start_hour, end_hour=end_hour, group=request.user.groups.all()[0])
            #serializer.save(start_hour=start_hour, end_hour=end_hour, group=request.user.groups.all()[0])
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def lecture_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        lecture = Lecture.objects.get(pk=pk)
    except Lecture.DoesNotExist:
        return JSONResponse({'status':101}, status=400)

    if request.method == 'GET':
        serializer = LectureDetail(lecture)
        data = serializer.data
        #problems
        #data['want_sign'] = serializers.serialize('json', lecture.student_want_sign.all())
        return JSONResponse(data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LectureSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        lecture.delete()
        return HttpResponse(status=204)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def swipe_student(request):
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        id = data['id']
        try:
            sign = Sign.objects.get(id=id)
        except Sign.DoesNotExist:
            return JSONResponse({'status':120}, status=400)
        if sign.status == 1:
            return JSONResponse({'status':121}, status=400)
        serializer = SwipeSerializer(sign, data=data)
        if serializer.is_valid():
            user = sign.student
            device = GCMDevice.objects.get(user=user)
            device.send_message(None,extra={"lecture_name": sign.lecture.name, "lecture_id":sign.lecture.id, "signer_name":request.user.name})
            serializer.save(id=id, status=1)
            user = request.user
            user.beer = user.beer + 1
            user.save()
            return JSONResponse({'beers':user.beer}, status=200)
        return JSONResponse(serializer.errors, status=400)

class MySigns(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSignSerializer
    def get(self, request, format=None):
        return Response(self.serializer_class(request.user).data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def sign_pic(request, id):
    if request.method == 'GET':
        try:
            user = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return JSONResponse({'status':130}, status=400)
        try:
            picture = user.sign_pic.url
        except ValueError:
            return JSONResponse({'status':131}, status=400)
        return JSONResponse({'picture':picture}, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def top_signers(request):
    group = request.user.groups.all()[0]
    try:
        user = Student.objects.filter(groups=group).order_by('-beer')[:10]
    except:
        return JSONResponse({'status':150}, status=400)
    serializer = TopSignerSerializer(user, many=True)
    data = {"comrades": serializer.data}
    return JSONResponse(data, status=200)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def register_device(request):
    token = request.DATA.get('device_token', '')

    device, created = GCMDevice.objects.get_or_create(user=request.user)
    device.registration_id = token
    device.active = True
    device.save()

    if created:
        return JSONResponse({'detail':'Device registered'}, status=200)
    else:
        return JSONResponse({'detail':'Device updated'}, status=200)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_password(request):
        data = JSONParser().parse(request)
        serializer = PasswordChangeSerializer(data=data)
        password = data['password']
        user = request.user
        if serializer.is_valid():
            if check_password(password, user.password):
                user.set_password(data['new_password'])
                user.save()
                #changed by Pejic
                return JSONResponse({'changed':True}, status=200)
            else:
                return JSONResponse({'status':170}, status=400)
        return JSONResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_name(request):
        data = JSONParser().parse(request)
        user = request.user
        serializer = NameChangeSerializer(data=data)
        if serializer.is_valid():
            user.name = data['name']
            user.save()
            return JSONResponse({'name':user.name}, status=200)
        else:
            return JSONResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def upload_sign_pic(request):
    data = request.data
    serializer = PhotoUploadSerializer(data=data)
    if serializer.is_valid():
        user = request.user
        if user.sign_pic is not None:
            user.sign_pic.delete()
        try:
            user.sign_pic = data['picture']
        except:
            return JSONResponse({'status':180}, status=400)
        user.save()
        return JSONResponse({"url": user.sign_pic.url}, status=200)
    return JSONResponse({'status':181}, status=400)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def request_sign(request):
    #data = JSONParser().parse(request)
    user = request.user
    try:
        lecture = Lecture.objects.get(id=request.data['lecture_id'])
    except:
        return JSONResponse({'status':190}, status=400)
    try: 
        Sign.objects.get(student=user, lecture=lecture)
    except:
        Sign.objects.create(student=user, lecture=lecture, status=0)
        if user.beer > 0:
            user.beer = user.beer - 1
            user.save()
        else:
            return JSONResponse({'status':192}, status=400)
        return JSONResponse({'sign_requested':True, 'beers':user.beer}, status=200)
    return JSONResponse({'status':191}, status=400)
