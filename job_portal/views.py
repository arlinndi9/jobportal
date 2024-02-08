from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from job_portal.forms import JobApplicationForm, JobForm
from job_portal.models import Job

# Create your views here.
def index(request):
    j=Job.objects.all()[:3]
    context={
        'j':j
    }
    return render(request,'index.html',context)

def job_list(request):
    j=Job.objects.all()
    for job in j:
        if job.is_expired():
            job.delete()
    jcount=Job.objects.all().count()
    paginator = Paginator(j, 6)#3 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'j':page_obj,
        'jcount':jcount,
        'page_obj':page_obj
    }
    return render(request,'job_listing.html',context)

def edit_job(request,job_id):
    job=get_object_or_404(Job,id=job_id)
    if job.posted_by != request.user:
        return redirect('joblist')

    if request.method=='POST':
        job.title=request.POST['title']
        job.description = request.POST['description']
        job.category = request.POST['category']
        job.requirements = request.POST['requirements']
        job.bonus_skills = request.POST['bonus_skills']
        job.name_company = request.POST['name_company']
        job.about_company = request.POST['about_company']
        job.location = request.POST['location']
        job.expiration_date = request.POST['expiration_date']
        job.save()

        return redirect('job_detail', job_id=job.id)  # Redirect to the job detail page after editing
    return render(request, 'edit_job.html', {'job': job})


def delete_job(request,job_id):
    job=Job.objects.get(id=job_id)
    if job.posted_by !=request.user:
        return redirect('joblist')

    else:
        job.delete()
        return redirect('joblist')

def job_search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all()
    context = {
        'jobs': jobs
    }
    return render(request, 'job_listing.html', context)



def job_detail(request,job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def calculate_salary(request):
    if request.method == 'POST':
        paga_bruto = float(request.POST.get('paga_bruto'))
        if paga_bruto <= 0:
            context = {'error': 'Paga bruto duhet te jete nje numer pozitiv dhe jo-zero.'}
            return render(request, 'index.html', context)
        kontributi_punetorit = 0.05
        kontributi_punedhenesit = 0.05
        paga_tatueshme = paga_bruto - paga_bruto * kontributi_punedhenesit
        # perqindja e tatimeve sipas pages
        t1 = 0.0
        t2 = 0.04
        t3 = 0.08
        t4 = 0.1
        tatimi1 = 0
        tatimi2 = 80
        tatimi3 = 250
        tatimi4 = 450
        paga_neto=0
        if 0 < paga_tatueshme <= 80:
            t = (tatimi2 - tatimi1) * t1
            paga_neto = paga_tatueshme - paga_tatueshme * t1 - t
        elif 80 < paga_tatueshme <= 250:
            t = (paga_tatueshme - tatimi2) * t2 + (tatimi2 - tatimi1) * t1
            paga_neto = paga_tatueshme - t
        elif 250 < paga_tatueshme <= 450:
            t = (paga_tatueshme - tatimi3) * t3 + (tatimi3 - tatimi2) * t2
            paga_neto = paga_tatueshme - t
        elif paga_tatueshme > 450:
            t = (paga_tatueshme - tatimi4) * t4 + (tatimi4 - tatimi3) * t3 + (tatimi3 - tatimi2) * t2
            paga_neto = paga_tatueshme - t

        context = {
            'paga_bruto': paga_bruto,
            'kontributi_punetorit': round(paga_bruto * kontributi_punetorit, 2),
            'kontributi_punedhenesit': round(paga_bruto * kontributi_punedhenesit, 2),
            'paga_tatueshme': round(paga_tatueshme, 2),
            'paga_0_80':round((tatimi2 - tatimi1) * t1, 2),
            'paga_neto': round(paga_neto, 2),
            't': round(t, 2)
        }
        return render(request, 'calculate_salary.html', context)

    return render(request, 'calculate_salary.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        name = request.POST['name']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        # Perform validation and create a new user
        if password == confirm_password:
            # Check if the email is already registered
            if User.objects.filter(email=email).exists():
                error_message = "Email address is already registered."
                return render(request, 'signup.html', {'error_message': error_message})

            # Create a new user with a unique email as the username
            user = User.objects.create_user(username=username, password=password, email=email, first_name=name,
                                            last_name=lastname)
            user.save()

            # Log in the user
            user = authenticate(username=email, password=password)
            login(request, user)

            # Redirect to a success page or homepage
            return redirect('index')
        else:
            # Passwords do not match, handle the error
            error_message = "Passwords do not match."
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')


def apply_for_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Add the job title to the form data
            form.instance.job_title = job.title
            form.save()  # Save the form data as a new JobApplication instance
            return redirect('index')  # Redirect to a success page
    else:
        form = JobApplicationForm()

    return render(request, 'apply_for_job.html', {'form': form, 'job': job})


# def apply_for_job(request):
#     if request.method == 'POST':
#         form = JobApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # Save the form data as a new JobApplication instance
#             return redirect('index')  # Redirect to a success page
#     else:
#         form = JobApplicationForm()
#
#     return render(request, 'apply_for_job.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('index')


# @login_required
# def create_job(request):
#     if request.method == 'POST':
#         title=request.POST['title']
#         description=request.POST['description']
#         category=request.POST['category']
#         requirements=request.POST['requirements']
#         bonus=request.POST['bonus_skills']
#         namecompany=request.POST['name_company']
#         aboutcompany=request.POST['about_company']
#         location=request.POST['location']
#         expiredate=request.POST['expiration_date']
#         j=Job.objects.create(title=title,description=description,category=category,
#                            requirements=requirements,bonus_skills=bonus,name_company=namecompany,about_company=aboutcompany,location=location,expiration_date=expiredate)
#         j.save()
#     return render(request,'postjob.html')

def create_job(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        requirements = request.POST['requirements']
        bonus_skills = request.POST['bonus_skills']
        name_company = request.POST['name_company']
        about_company = request.POST['about_company']
        location = request.POST['location']
        expiration_date = request.POST['expiration_date']

        job = Job.objects.create(
            title=title,
            description=description,
            category=category,
            requirements=requirements,
            bonus_skills=bonus_skills,
            name_company=name_company,
            about_company=about_company,
            location=location,
            expiration_date=expiration_date,
            posted_by=request.user  # Assign the current user as the job poster
        )

        return redirect('joblist')  # Redirect to a success page or job list

    return render(request, 'postjob.html')