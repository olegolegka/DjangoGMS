from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import PlanSerializer
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from .models import *
from django.contrib.auth.models import User
# Create your views here.


def Home(request):
    if not request.user.is_active:
        return redirect('login')
    return render(request, 'index.html')


def About(request):
    return render(request, 'about.html')


def Contact(request):
    return render(request, 'contact.html')
def Profile(request):
    return render(request, 'profile.html')



def Login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']

        user = authenticate(username=u, password=p)
        try:
            if user.is_active:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'login.html', d)


def Logout(request):
    if not request.user.is_active:
        return redirect('login')
    logout(request)
    return redirect('login')


def Add_Enquiry(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['emailid']
        a = request.POST['age']
        g = request.POST['gender']
        try:
            Enquiry.objects.create(
                name=n, contact=c, emailid=e, age=a, gender=g)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_enquiry.html', d)


def View_Enquiry(request):
    enq = Enquiry.objects.all()
    d = {'enq': enq}
    return render(request, 'view_enquiry.html', d)
def Delete_Enquiry(request,pid):
    enquiry = Enquiry.objects.get(id=pid)
    enquiry.delete()
    return redirect('view_enquiry')


def Add_Equipment(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        p = request.POST['price']
        u = request.POST['unit']
        d = request.POST['date']
        desc = request.POST['desc']
        try:
            Equipment.objects.create( name=n, price=p, unit=u, date=d, description=desc)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_equipment.html', d)


def View_Equipment(request):
    equ = Equipment.objects.all()
    d = {'equ': equ}
    return render(request, 'view_equipment.html', d)

def Delete_Equipment(request,pid):
    equipment = Equipment.objects.get(id=pid)
    equipment.delete()
    return redirect('view_equipment')

def Add_Plan(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        a = request.POST['amount']
        d = request.POST['duration']
        try:
            Plan.objects.create( name=n, amount=a, duration=d)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_plan.html', d)


def View_Plan(request):
    pln = Plan.objects.all()
    d = {'pln': pln}
    return render(request, 'view_plan.html', d)

def Delete_Plan(request,pid):
    plan = Plan.objects.get(id=pid)
    plan.delete()
    return redirect('view_plan')

def Add_Member(request):
    error = ""
    plan1 = Plan.objects.all()
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['emailid']
        a = request.POST['age']
        g = request.POST['gender']
        p = request.POST['plan']
        joindate = request.POST['joindate']
        expiredate = request.POST['expdate']
        initialamount = request.POST['initialamount']
        plan = Plan.objects.filter(name=p).first()
        try:
            Member.objects.create( name=n, contact=c,emailid=e, age=a,gender=g,plan=plan, joindate=joindate, expiredate = expiredate, initialamount = initialamount)
            error = "no"
        except:
            error = "yes"
    d = {'error': error, 'plan':plan1}
    return render(request, 'add_member.html', d)


def View_Member(request):
    search_query = request.GET.get('search', '')
    if search_query:
        member = Member.objects.filter(Q(name__icontains = search_query) |  Q(emailid__icontains = search_query) | Q(plan__icontains = search_query) | Q(expiredate__icontains = search_query))
    else:
        member = Member.objects.all()
    d = {'member': member}
    return render(request, 'view_member.html', d)

def Delete_Member(request,pid):
    member = Member.objects.get(id=pid)
    member.delete()
    return redirect('view_member')
#Объявление сериализатора для APi в файле serializers
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all().order_by('name')
    serializer_class = PlanSerializer




