from django.conf.urls import url, patterns, include
from restful import views as _views

urlpatterns = [
        url(r'lectures/$', _views.lecture_list),
        url(r'lecture/(?P<pk>[0-9]+)/$', _views.lecture_detail),
        url(r'swipe/$', _views.swipe_student),
        url(r'mysign/$', _views.MySigns.as_view(), name='mysigns'),
        url(r'signpic/(?P<id>[0-9]+)/$', _views.sign_pic, name='signpic'),
        url(r'top/$', _views.top_signers, name='top_signers'),
        url(r'mysignpic/$', _views.upload_sign_pic, name='mysignpic'),
        url(r'register/?', _views.register_device, name='register_device'),
        url(r'passchange/?', _views.change_password, name='change_password'),
        url(r'namechange/?', _views.change_name, name='change_name'),
        url(r'signrequest/?', _views.request_sign, name='request_sign'),
]
