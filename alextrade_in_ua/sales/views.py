# coding: utf-8

import time
import re
import urllib

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt

from .models import Tvr, StaticContent, Nkls


@csrf_exempt
@login_required(login_url='/login/')
def adminpage(request, **vargs):
    user = request.user
    try:
        ostdate = StaticContent.objects.get(nam='Ostdate')
    except:
        ostdate = ""
    try:
        tvrdate = StaticContent.objects.get(nam='Tvrdate')
    except:
        tvrdate = ""
    if user:
        try:
            sprtvr = StaticContent.objects.get(nam='Tvr')
        except:
            sprtvr = ""
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
        elif user.username.find("oper") != -1:
            return render(request, "role-oper.html", template_values)
        else:
            return render(request, "role-agent.html", template_values)


def dict_to_str(d, lev=0):
    res = """<ul class="lev%s">""" % lev
    items = list(d.items())

    def cmp2(a):
        if type(a[1]) == type({}):
            return a[0]
        return a[1][0]

    items.sort(key=cmp2)
    for key, val in items:
        if type(d[key]) == type({}):
            res += "<li>%s%s</li>" % (key, dict_to_str(d[key], lev + 1))
        else:
            res += """<li class="node"><span class="nam">%s</span><span class="c7">%s</span><span class="c1">%s</span><span class="c2">%s</span><span class="c3">%s</span><span class="c4">%s</span><span class="cnt">%s</span><input class="val" type="number" name="%s" /></li>""" % tuple(
                d[key])
    res += "</ul>"
    return res


@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def uploadsprtvr(request, **vargs):
    if request.POST:
        try:
            content = request.FILES["csv"].read()
        except:
            content = ""
        if content:
            content = content.decode("utf-8").strip().split("\n")
            tvrs = {}
            tvrs_obj = []
            for t in content:
                id, prz_g1, prz_g2, typ, nam, c7, c4, c3, c2, c1, k = t.strip().split("\t")
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
                tvr.c7 = float(c7)
                tvr.save()
                tvrs_obj.append(tvr)

                if tvr.prz_g1 not in tvrs:
                    tvrs[tvr.prz_g1] = {}
                if tvr.prz_g1 != tvr.prz_g2:
                    if tvr.prz_g2 not in tvrs[tvr.prz_g1]:
                        tvrs[tvr.prz_g1][tvr.prz_g2] = {}
                if tvr.prz_g2 in tvrs[tvr.prz_g1]:
                    tvrs[tvr.prz_g1][tvr.prz_g2][tvr.id] = (
                    tvr.nam, tvr.c7, tvr.c4, tvr.c3, tvr.c2, tvr.c1, int(tvr.k), tvr.id)
                else:
                    tvrs[tvr.prz_g1][tvr.id] = (tvr.nam, tvr.c7, tvr.c4, tvr.c3, tvr.c2, tvr.c1, int(tvr.k), tvr.id)

            content, created = StaticContent.objects.get_or_create(nam="Tvr")
            content.val = dict_to_str(tvrs, 0)
            content.save()

            tvrdate, created = StaticContent.objects.get_or_create(nam="Tvrdate")
            tvrdate.val = time.strftime("%d.%m.%y %H:%M:%S", time.gmtime())
            tvrdate.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True});

        return redirect("/sales/")


@csrf_exempt
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


@csrf_exempt
@user_passes_test(lambda u: u.is_staff)
def uploadost(request, **vargs):
    if request.POST:
        #    ost, created = StaticContent.objects.get_or_create(nam='Tvr')

        try:
            content = request.FILES["csv"].read()
        except:
            content = ""
        if content:
            content = content.decode("utf-8").strip().split("\n")
            tvrs = {}
            for t in content:
                id, k = t.strip().split("\t")
                try:
                    tvr = Tvr.objects.get(id=int(id))
                except:
                    continue
                tvr.k = float(k)
                tvr.save()
                #        p = re.compile('(<span class="cnt">)(-?\d+\.?\d?)(</span><input class="val" type="number" name="%s" />)' % id)
                #        ost.val = p.sub(lambda x: x.group(1)+k+x.group(3), ost.val)

                #    ost.save()
                if tvr.prz_g1 not in tvrs:
                    tvrs[tvr.prz_g1] = {}
                if tvr.prz_g1 != tvr.prz_g2:
                    if tvr.prz_g2 not in tvrs[tvr.prz_g1]:
                        tvrs[tvr.prz_g1][tvr.prz_g2] = {}
                if tvr.prz_g2 in tvrs[tvr.prz_g1]:
                    tvrs[tvr.prz_g1][tvr.prz_g2][tvr.id] = (
                    tvr.nam, tvr.c7, tvr.c4, tvr.c3, tvr.c2, tvr.c1, int(tvr.k), tvr.id)
                else:
                    tvrs[tvr.prz_g1][tvr.id] = (tvr.nam, tvr.c7, tvr.c4, tvr.c3, tvr.c2, tvr.c1, int(tvr.k), tvr.id)

            content, created = StaticContent.objects.get_or_create(nam="Tvr")
            content.val = dict_to_str(tvrs, 0)
            content.save()

        ostdate, created = StaticContent.objects.get_or_create(nam="Ostdate")
        ostdate.val = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime())
        ostdate.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True});

        return redirect("/sales/")


@csrf_exempt
@login_required(login_url='/login/')
def savenkl(request, **vargs):
    if request.POST:
        ost, created = StaticContent.objects.get_or_create(nam='Tvr')

        def repl(match):
            cnt = float(match.group(2))
            return match.group(1) + str(cnt) + match.group(3)

        client = request.POST.get("client", "???")
        txt = []
        params = map(lambda x: tuple(x.split("=")), request.body.decode("utf-8").split("&"))
        for key, val in params:
            if key != "client":
                try:
                    val = int(val)
                except:
                    val = 0
                if val:
                    p = re.compile(
                        '(<span class="cnt">)(-?\d+\.?\d?)(</span><input class="val" type="number" name="%s" />)' % key)
                    ost.val = p.sub(lambda x: x.group(1) + str(float(x.group(2)) - val) + x.group(3), ost.val)
                    txt.append(u"\t".join((key, str(val),)))
        txt = u"\n".join(txt)

        nkl = Nkls()
        nkl.user = request.user
        nkl.client = client
        nkl.downloads = 0
        nkl.val = txt
        nkl.save()

        ost.save()

        return redirect("/sales/")

    try:
        nkl = Nkls.objects.get(id=request.GET.get("id", None))
    except:
        nkl = None
    if nkl:
        client = urllib.parse.quote(nkl.client.encode("utf-8"))
        fn = "attachment; filename=%s_%s.csv" % (nkl.date, client)

        response = HttpResponse(nkl.val)
        response['Content-Type'] = 'text/csv'
        response['Content-Disposition'] = fn

        nkl.downloads += 1
        nkl.save()

        return response

    return redirect("/sales/")


@csrf_exempt
@user_passes_test(lambda u: u.is_staff)
def delnkl(request, **vargs):
    try:
        nkl = Nkls.objects.get(id=request.GET.get("id", None))
    except:
        nkl = None
    if nkl:
        nkl.delete()

    return redirect("/sales/")


def frontend(request, **vargs):
    return render(request, 'frontend.html', {})
