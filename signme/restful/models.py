import os
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from authemail.models import EmailUserManager, EmailAbstractUser



def get_image_path(instance, filename):
    """Correctly organize user images
    """
    return os.path.join('static', 'images', str(instance.id), filename)

class Student(EmailAbstractUser):
    # Custom fields
    date_of_birth = models.DateField('Date of birth', null=True,
        blank=True)
    beer = models.IntegerField(default=10)
    # Default picture
    sign_pic = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    # Required
    objects = EmailUserManager()

@receiver(post_save, sender=Student)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)

# Create your models here.


class Lecture(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_hour = models.DateTimeField()
    end_hour = models.DateTimeField()
    student_want_sign = models.ManyToManyField(Student, blank=True, through='Sign')
    # should remove blank = True in future, because of mental overhead to 
    # make group for every lecture
    group = models.ForeignKey(Group, null=True)

    class Meta:
        ordering = ['start_hour']

    @property
    def count_student_want_sign(self):
       return self.student_want_sign.count()

    def get_normal_start_time(self):
        desired = '%H-%M'
        result = self.start_hour.strftime(desired)
        return result

    def get_normal_end_time(self):
        desired = '%H-%M'
        result = self.end_hour.strftime(desired)
        return result

    def __unicode__(self):
        return self.name

class Sign(models.Model):
    student = models.ForeignKey(Student)
    lecture = models.ForeignKey(Lecture)
    # 0 want's sign, 1 signed
    status = models.IntegerField(default=0)
   
    class Meta:
        ordering = ['status'] 

    def __unicode__(self):
        return self.student.name + self.lecture.name
