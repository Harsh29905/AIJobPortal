from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import recruiter_required
from recruiters.models import RecruiterProfile
from candidates.models import CandidateProfile
from .models import Job, JobSkill
from .forms import JobForm
from applications.models import Application
from recommendations.services import calculate_resume_job_match


def home(request):
    featured_jobs = Job.objects.filter(status='open').select_related('recruiter').prefetch_related('skills')[:6]
    recent_jobs = Job.objects.filter(status='open').select_related('recruiter').prefetch_related('skills')[6:12]
    
    total_jobs_count = Job.objects.filter(status='open').count()
    total_companies_count = RecruiterProfile.objects.count()
    total_candidates_count = CandidateProfile.objects.count()

    context = {
        'featured_jobs': featured_jobs,
        'recent_jobs': recent_jobs,
        'total_jobs_count': total_jobs_count,
        'total_companies_count': total_companies_count,
        'total_candidates_count': total_candidates_count,
    }
    return render(request, 'jobs/home.html', context)


def job_list(request):
    jobs_queryset = Job.objects.filter(status='open').select_related('recruiter').prefetch_related('skills')

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        jobs_queryset = jobs_queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(recruiter__company_name__icontains=q) |
            Q(skills__skill_name__icontains=q)
        ).distinct()

    # Location filter
    location = request.GET.get('location', '').strip()
    if location:
        jobs_queryset = jobs_queryset.filter(location__icontains=location)

    # Work Arrangement filter
    work_arrangement = request.GET.get('work_arrangement', '').strip()
    if work_arrangement:
        jobs_queryset = jobs_queryset.filter(work_arrangement=work_arrangement)

    # Employment Type filter
    employment_type = request.GET.get('employment_type', '').strip()
    if employment_type:
        jobs_queryset = jobs_queryset.filter(employment_type=employment_type)

    # Experience Level filter
    experience_level = request.GET.get('experience_level', '').strip()
    if experience_level:
        jobs_queryset = jobs_queryset.filter(experience_level=experience_level)

    # Pagination: 6 jobs per page
    paginator = Paginator(jobs_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Preserve search query parameters in pagination links
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        'jobs': page_obj,
        'page_obj': page_obj,
        'q': q,
        'location': location,
        'selected_work_arrangement': work_arrangement,
        'selected_employment_type': employment_type,
        'selected_experience_level': experience_level,
        'query_params': query_params.urlencode(),
        'total_results': jobs_queryset.count(),
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, job_id):
    job = get_object_or_404(Job.objects.select_related('recruiter').prefetch_related('skills'), id=job_id)
    
    user_application = None
    ai_match_preview = None
    is_recruiter_owner = False

    if request.user.is_authenticated:
        if request.user.is_candidate:
            candidate_profile = getattr(request.user, 'candidate_profile', None)
            if candidate_profile:
                user_application = Application.objects.filter(job=job, candidate=candidate_profile).first()
                # Compute live match preview for the candidate
                ai_match_preview = calculate_resume_job_match(
                    candidate_profile.extracted_resume_text,
                    candidate_profile.get_all_skills_list(),
                    job
                )
        elif request.user.is_recruiter:
            if hasattr(request.user, 'recruiter_profile') and job.recruiter == request.user.recruiter_profile:
                is_recruiter_owner = True

    context = {
        'job': job,
        'user_application': user_application,
        'ai_match_preview': ai_match_preview,
        'is_recruiter_owner': is_recruiter_owner,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
@recruiter_required
def job_create(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(recruiter=profile)
            messages.success(request, f"Job posting '{job.title}' created successfully!")
            return redirect('recruiter_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Create New Job Opening'})


@login_required
@recruiter_required
def job_edit(request, job_id):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id, recruiter=profile)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save(recruiter=profile)
            messages.success(request, f"Job '{job.title}' updated successfully.")
            return redirect('recruiter_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'title': f'Edit: {job.title}', 'job': job})


@login_required
@recruiter_required
def job_toggle_status(request, job_id):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id, recruiter=profile)
    
    if job.status == 'open':
        job.status = 'closed'
        messages.info(request, f"Job '{job.title}' is now closed.")
    else:
        job.status = 'open'
        messages.success(request, f"Job '{job.title}' is now open.")
    job.save()
    return redirect('recruiter_dashboard')


@login_required
@recruiter_required
def job_delete(request, job_id):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id, recruiter=profile)
    
    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f"Job posting '{title}' was deleted.")
        return redirect('recruiter_dashboard')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})
