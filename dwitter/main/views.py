# -*- coding: utf-8 -*- 
import re
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from dwitter.main.models import Member, Dwit, DPF
from dwitter.main.tasks import celery_dwitsaved, celery_follow, celery_unfollow
from dwitter.main.forms import MemberForm, SearchForm
from django.utils import translation

@login_required
@ensure_csrf_cookie
def home(request):
    if not request.session.get('django_language', None):
        request.session['django_language'] = get_language()
    me = request.user.member
    following = me.following.all().count()
    followers = me.followers.all().count()
    nodwits = Dwit.objects.filter(member=me).count()
    context_vars={'me':me,'following':following,'followers':followers,'nodwits':nodwits,'navbar':'home'}
    if request.GET.get('tag'):
        context_vars.update({'tag':request.GET['tag']})
    template_name='home.html'
    context = RequestContext(request)
    return render_to_response(template_name,context_vars,context_instance=context)

@login_required
def getflow(request, nfd):
    nod = settings.NUMBER_OF_DWITS
    context_vars = {}
    if request.GET.get('tag'):
        dwits = Dwit.objects.filter(tags__name=request.GET.get('tag'))[int(nfd):int(nfd)+int(nod)]
    elif request.GET.get('username'):
        me = get_object_or_404(Member, user__username=request.GET['username'])
        dwits = Dwit.objects.filter(member = me)[int(nfd):int(nfd)+int(nod)]
        context_vars.update({'profile':True})
    elif request.GET.get('hash'):
        form = SearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data.get('hash'):
                hashes = form.cleaned_data['hash']
                hashes = hashes.replace(',','')
                hashes_array = hashes.split()
                dwits = Dwit.objects.filter(tags__name__in=hashes_array).distinct()[int(nfd):int(nfd)+int(nod)]
                context_vars.update({'search':True})
    else:
        me = request.user.member
        dwitspf = DPF.objects.filter(member = me)[int(nfd):int(nfd)+int(nod)]
        dwits=[]
        for dwitpf in dwitspf:
            dwits.append(dwitpf.dwit)
    for dwit in dwits:
        dwit.content = re.subn('(?P<tag>(?<= #)\w+)','<a href="/main/home/?tag=\g<tag>" class="label label-info vmiddle" rel="nofollow" title="\g<tag>">#\g<tag></a>',dwit.content)[0].replace("#<","<")
    template_name='flow.html'
    context_vars.update({'dwits':dwits})
    if len(dwits) == nod:
        context_vars.update({'nfd':int(nfd)+nod})
    context = RequestContext(request)
    return render_to_response(template_name,context_vars,context_instance=context)

@login_required
def gettags(request):
    notags = settings.NUMBER_OF_TAGS
    tags = Dwit.tags.most_common()[0:notags]
    context_vars={'tags':tags}
    template_name='tags.html'
    context = RequestContext(request)
    return render_to_response(template_name,context_vars,context_instance=context)

@login_required
def dwit(request):
    if request.method != 'POST':
        response = HttpResponse(mimetype="text/html")
        response['content-type']="text/html; charset=UTF-8"
        response.write(u"POST only!.")
        return response
    me = request.user.member
    if request.POST.get('dwit'):
        content = escape(request.POST['dwit'])
        direct = False
        if re.match('^\@\w+',content):
            try:
                Member.objects.get(user__username=re.match('^\@\w+',content).group(0)[1:])
                direct = True
            except Member.DoesNotExist:
                response = HttpResponse(mimetype="application/json")
                response.write(u'{"status":"error","message":"'+_('No sush user.')+'"}')
                return response
        tags = re.findall(r' #\w+',content)
        try:
            replyto = Dwit.objects.get(pk = request.POST.get('dwitid',None))
        except Dwit.DoesNotExist:
            replyto = None
        dwit = Dwit.objects.create(member = me, content = content, replyto = replyto, direct=direct)
        for tag in tags:
            dwit.tags.add(tag[2:])
        rendered = render_to_string('flow.html',{'dwits':[dwit]})
        celery_dwitsaved.delay(dwit, rendered)
    elif request.POST.get('dwitid'):
        dwit = get_object_or_404(Dwit, pk=request.POST['dwitid'])
        newdwit = Dwit.objects.create(member = me, content = dwit.content, redwit = dwit.member)
        if dwit.tags:
            tags = dwit.tags.all()
            newdwit.tags.add(*tags)
        rendered = render_to_string('flow.html',{'dwits':[newdwit]})
        celery_dwitsaved.delay(newdwit, rendered)
    response = HttpResponse(mimetype="application/json")
    response.write('{"status":"success","message":"'+_('Dwit published.')+'"}')
    return response

@login_required
@ensure_csrf_cookie
def profile(request,username):
    m = get_object_or_404(Member, user__username=username)
    nodwits = Dwit.objects.filter(member=m).count()
    fing = m.following.all()
    following = len(fing)
    if request.user.username != username:
        me = request.user.member
        me_fing = me.following.all()
        if m in me_fing:
            action = 'unfollow'
        else:
            action = 'follow'
    else:
        action = None
    fers = m.followers.all()
    followers = len(fers)
    context_vars={'m':m,'fing':fing,'fers':fers,'action':action,'nodwits':nodwits,'following':following,'followers':followers,'navbar':'profile'}
    if not action:
        if request.method == 'POST':
            form = MemberForm(request.POST, request.FILES, instance=m)
            if form.is_valid():
                if request.LANGUAGE_CODE != form.cleaned_data['language']:
                    request.session['django_language'] = form.cleaned_data['language']
                    translation.activate(form.cleaned_data['language'])
                form.save()
                context_vars.update({'success':_('Changes saved'),'form':form,'current_lang':m.language})
            else:
                ferrors = ''
                for field in form:
                    if field.errors:
                        ferrors += '<b>'+field.label+'</b>: '
                        for error in field.errors:
                            ferrors += error+'<br />'
                context_vars.update({'ferrors':ferrors,'form':form,'current_lang':m.language})
        else:
            form = MemberForm(instance=m)
            context_vars.update({'form':form,'current_lang':m.language})
    template_name='profile.html'
    context = RequestContext(request)
    return render_to_response(template_name,context_vars,context_instance=context)

@login_required
def follow(request, username):
    m = get_object_or_404(Member, user__username=username)
    me = request.user.member
    me.following.add(m)
    celery_follow.delay(me, m)
    response = HttpResponse(mimetype="text/html")
    response['content-type']="text/html; charset=UTF-8"
    response.write(_('You follow %s') % username)
    return response

@login_required
def unfollow(request, username):
    m = get_object_or_404(Member, user__username=username)
    me = request.user.member
    me.following.remove(m)
    celery_unfollow.delay(me,m)
    response = HttpResponse(mimetype="text/html")
    response['content-type']="text/html; charset=UTF-8"
    response.write(_('You stopped following %s') % username)
    return response

@login_required
def search(request):
    form = SearchForm()
    context_vars={'form':form,'navbar':'search'}
    template_name='search.html'
    context = RequestContext(request)
    return render_to_response(template_name,context_vars,context_instance=context)

@login_required
def getdwit(request,dwit):
    d = get_object_or_404(Dwit, pk=dwit)
    template_name='redwit.html'
    context = RequestContext(request)
    return render_to_response(template_name,{'dwit':d},context_instance=context) 

@login_required
def getreplyto(request,dwit):
    d = get_object_or_404(Dwit, pk=dwit)
    template_name='replyto.html'
    context = RequestContext(request)
    return render_to_response(template_name,{'dwit':d},context_instance=context) 

