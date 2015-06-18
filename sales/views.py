# coding: utf-8

import time
import re
import urllib

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from models import Tvr, StaticContent, Nkls

@login_required(login_url='/login/')
def adminpage(request, **vargs):
  user = request.user
  try: ostdate = StaticContent.objects.get(nam='Ostdate')
  except: ostdate = ""
  try: tvrdate = StaticContent.objects.get(nam='Tvrdate')
  except: tvrdate = ""
  if user:
    try: sprtvr = StaticContent.objects.get(nam='Tvr')
    except: sprtvr = ""
    if sprtvr:
      sprtvr = sprtvr.val
    else:
      sprtvr = ""

    nkls = Nkls.objects.all().order_by("-date")
    template_values = {
      'title': u"www.alextrade.in.ua",
      'user': user,
      'logout_url': "/logout/",
      'sprtvr': sprtvr,
      'nkls': nkls,
      'ostdate': ostdate,
      'tvrdate': tvrdate,
    }
    if user.is_superuser:
      return render(request, "role-admin.html", template_values)
    elif user.username.find("oper") <> -1:
      return render(request, "role-oper.html", template_values)
    else:
      return render(request, "role-agent.html", template_values)

def dict_to_str(d, lev=0):
  res = """<ul class="lev%s">""" % lev
  items = d.items()
  def cmp2(a,b):
    if type(a[1])==type({}) or type(b[1])==type({}):
      return cmp(a[0], b[0])
    return cmp(a[1], b[1])

  items.sort(cmp2)
  for key,val in items:
    if type(d[key]) == type({}):
      res+="<li>%s%s</li>" % (key, dict_to_str(d[key],lev+1))
    else:
      res+="""<li class="node"><span class="nam">%s</span><span class="c1">%s</span><span class="c2">%s</span><span class="c3">%s</span><span class="c4">%s</span><span class="cnt">%s</span><input class="val" type="number" name="%s" /></li>""" % tuple(d[key])
  res+="</ul>"
  return res

@user_passes_test(lambda u: u.is_superuser)
def uploadsprtvr(request, **vargs):
  if request.POST:
    try: content = request.FILES["csv"].read()
    except: content = ""
    if content:
      content = unicode(content, "utf-8").strip().split("\n")
      tvrs = {}
      tvrs_obj = []
      for t in content:
        id,prz_g1,prz_g2,typ,nam,c4,c3,c2,c1,k = t.strip().split("\t")
        tvr, created = Tvr.objects.get_or_create(id=id)
        tvr.prz_g1 = prz_g1
        tvr.prz_g2 = prz_g2
        tvr.typ = typ
        tvr.nam = nam
        tvr.k = float(k)
        tvr.c1 = float(c1)
        tvr.c2 = float(c2)
        tvr.c3 = float(c3)
        tvr.c4 = float(c4)
        tvr.save()
        tvrs_obj.append(tvr)

        if not tvrs.has_key(tvr.prz_g1):
          tvrs[tvr.prz_g1] = {}
        if tvr.prz_g1 <> tvr.prz_g2:
          if not tvrs[tvr.prz_g1].has_key(tvr.prz_g2):
            tvrs[tvr.prz_g1][tvr.prz_g2] = {}
        if tvrs[tvr.prz_g1].has_key(tvr.prz_g2):
          tvrs[tvr.prz_g1][tvr.prz_g2][tvr.id] = (tvr.nam, tvr.c4,tvr.c3,tvr.c2,tvr.c1,int(tvr.k), tvr.id)
        else:
          tvrs[tvr.prz_g1][tvr.id] = (tvr.nam, tvr.c4,tvr.c3,tvr.c2,tvr.c1,int(tvr.k), tvr.id)
                    	
      content, created = StaticContent.objects.get_or_create(nam="Tvr")
      content.val = dict_to_str(tvrs, 0)
      content.save()

      tvrdate, created = StaticContent.objects.get_or_create(nam="Tvrdate")
      tvrdate.val = time.strftime("%d.%m.%y %H:%M:%S", time.gmtime())
      tvrdate.save()

    return redirect("/sales/")

@user_passes_test(lambda u: u.is_superuser)
def clearsprtvr(request, **vargs):
  if request.POST:
    tvrs = Tvr.objects.all()
    for tvr in tvrs:
      tvr.delete()

    content, created = StaticContent.objects.get_or_create(nam="Tvr")
    if content and not created:
      content.delete()

    return redirect("/sales/")

@user_passes_test(lambda u: u.is_staff)
def uploadost(request, **vargs):
  if request.POST:
#    ost, created = StaticContent.objects.get_or_create(nam='Tvr')

    try: content = request.FILES["csv"].read()
    except: content = ""
    if content:
      content = unicode(content, "utf-8").strip().split("\n")
      tvrs = {}
      for t in content:
        id,k = t.strip().split("\t")
        try: tvr = Tvr.objects.get(id=int(id))
        except: continue
        tvr.k = float(k)
        tvr.save()
#        p = re.compile('(<span class="cnt">)(-?\d+\.?\d?)(</span><input class="val" type="number" name="%s" />)' % id)
#        ost.val = p.sub(lambda x: x.group(1)+k+x.group(3), ost.val)

#    ost.save()
        if not tvrs.has_key(tvr.prz_g1):
          tvrs[tvr.prz_g1] = {}
        if tvr.prz_g1 <> tvr.prz_g2:
          if not tvrs[tvr.prz_g1].has_key(tvr.prz_g2):
            tvrs[tvr.prz_g1][tvr.prz_g2] = {}
        if tvrs[tvr.prz_g1].has_key(tvr.prz_g2):
          tvrs[tvr.prz_g1][tvr.prz_g2][tvr.id] = (tvr.nam, tvr.c4,tvr.c3,tvr.c2,tvr.c1,int(tvr.k), tvr.id)
        else:
          tvrs[tvr.prz_g1][tvr.id] = (tvr.nam, tvr.c4,tvr.c3,tvr.c2,tvr.c1,int(tvr.k), tvr.id)
                    	
      content, created = StaticContent.objects.get_or_create(nam="Tvr")
      content.val = dict_to_str(tvrs, 0)
      content.save()

    ostdate, created = StaticContent.objects.get_or_create(nam="Ostdate")
    ostdate.val = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime())
    ostdate.save()

    return redirect("/sales/")

@login_required(login_url='/login/')
def savenkl(request, **vargs):
  if request.POST:
    ost, created = StaticContent.objects.get_or_create(nam='Tvr')

    def repl(match):
      cnt = float(match.group(2))
      return match.group(1)+str(cnt)+match.group(3)

    client = request.POST.get("client", "???")
    txt = []
    params = map(lambda x: tuple(x.split("=")), request.body.split("&"))
    for key,val in params:
      if key <> "client":
        try: val = int(val)
        except: val = 0
        if val:
          p = re.compile('(<span class="cnt">)(-?\d+\.?\d?)(</span><input class="val" type="number" name="%s" />)' % key)
          ost.val = p.sub(lambda x: x.group(1)+str(float(x.group(2))-val)+x.group(3), ost.val)
          txt.append(u"\t".join((key,str(val),)))
    txt = u"\n".join(txt)

    nkl = Nkls()
    nkl.user = request.user
    nkl.client = client
    nkl.downloads = 0
    nkl.val = txt
    nkl.save()

    ost.save()

    return redirect("/sales/")

  try: nkl = Nkls.objects.get(id=request.GET.get("id", None))
  except: nkl = None
  if nkl:
    client = urllib.quote(nkl.client.encode("utf-8"))
    fn = "attachment; filename=%s_%s.csv" % (nkl.date,client)

    response = HttpResponse(nkl.val)
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = fn

    nkl.downloads+=1
    nkl.save()

    return response

  return redirect("/sales/")

@user_passes_test(lambda u: u.is_staff)
def delnkl(request, **vargs):
  try: nkl = Nkls.objects.get(id=request.GET.get("id", None))
  except: nkl = None
  if nkl:
    nkl.delete()

  return redirect("/sales/")

def frontend(request, **vargs):
  return render(request, 'frontend.html', {})




