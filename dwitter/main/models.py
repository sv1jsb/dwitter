# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from registration.signals import user_activated
from taggit.managers import TaggableManager
from datetime import datetime

def uploadto(instance, filename):
    return instance.user.username+'/'+filename

class Member(models.Model):
    user = models.OneToOneField(User)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    nick = models.CharField(_(u'Name'), max_length=50)
    descr = models.TextField(_(u'Description'),blank=True)
    image = models.ImageField(_(u'Image'), upload_to=uploadto, default='none.png')
    language = models.CharField(_(u'Language'), max_length=5, default='en')

    def __unicode__(self):
        return self.user.username

class Dwit(models.Model):
    content = models.TextField()
    member = models.ForeignKey(Member)
    stamp = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)
    redwit = models.ForeignKey(Member, blank=True, null=True, related_name='redwitby')
    replyto = models.ForeignKey('self', blank=True, null=True, related_name='replyfrom')
    direct = models.BooleanField(blank=True)

    def _dwitter_stamp(self):
        t = datetime.now() - self.stamp
        if t.days > 0:
            return _(u'%dd') % t.days
        else:
            h = t.seconds / 3600
            if h > 0:
                return _(u'%dh') % h
            else:
                m = t.seconds / 60
                if m == 0: m = 1
                return _(u'%dm') % m

    dwitter_stamp = property(_dwitter_stamp)

    class Meta:
        ordering = ['-stamp']

class DPF(models.Model):    #Dwit Per Follower
    member = models.ForeignKey(Member, db_index=True)
    dwit = models.ForeignKey(Dwit)
    stamp = models.DateTimeField()

    class Meta:
        ordering = ['-stamp']

@receiver(user_activated)
def uactivated(sender, **kwargs):
    Member.objects.create(user=kwargs['user'], nick=kwargs['user'].username, language=kwargs['language'])
