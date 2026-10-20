from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import recruiter_required
from .models import RecruiterProfile
from .forms import RecruiterProfileForm
from jobs.models import Job
from applications.models import Application


@login_required
@recruiter_required
def recruiter_dashboard(request):
    profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)
    recruiter_jobs = Job.objects.filter(recruiter=profile).order_by('-created_at')
    
    total_jobs = recruiter_jobs.count()
    active_jobs = recruiter_jobs.filter(status='open').count()
    total_applications = Application.objects.filter(job__recruiter=profile).count()
    shortlisted_candidates = Application.objects.filter(
        job__recruiter=profile, status__in=['shortlisted', 'interview', 'hired']
    ).count()

    context = {
        'profile': profile,
        'jobs': recruiter_jobs,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'shortlisted_candidates': shortlisted_candidates,
    }
    return render(request, 'recruiters/dashboard.html', context)


@login_required
@recruiter_required
def recruiter_profile_edit(request):
    profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = RecruiterProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Company profile updated successfully.")
            return redirect('recruiter_dashboard')
    else:
        form = RecruiterProfileForm(instance=profile)
    return render(request, 'recruiters/profile_edit.html', {'form': form, 'profile': profile})


@login_required
@recruiter_required
def job_applicants(request, job_id):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id, recruiter=profile)
    
    status_filter = request.GET.get('status', '')
    applicants = Application.objects.filter(job=job).select_related('candidate', 'candidate__user')
    
    if status_filter:
        applicants = applicants.filter(status=status_filter)
        
    # Sort applicants by highest AI Match Score first
    applicants = applicants.order_by('-match_score', '-applied_at')

    context = {
        'job': job,
        'applicants': applicants,
        'selected_status': status_filter,
    }
    return render(request, 'recruiters/job_applicants.html', context)


@login_required
@recruiter_required
def applicant_detail(request, application_id):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    application = get_object_or_404(Application, id=application_id, job__recruiter=profile)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f"Application status updated to '{application.get_status_display()}'.")
            return redirect('applicant_detail', application_id=application.id)

    context = {
        'application': application,
        'candidate': application.candidate,
        'job': application.job,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'recruiters/applicant_detail.html', context)
