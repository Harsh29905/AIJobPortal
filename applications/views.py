from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from accounts.decorators import candidate_required, recruiter_required
from jobs.models import Job
from candidates.models import CandidateProfile
from .models import Application
from .forms import ApplicationForm
from recommendations.services import (
    calculate_resume_job_match,
    extract_text_from_pdf,
    extract_skills_from_text,
)


@login_required
@candidate_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    candidate = get_object_or_404(CandidateProfile, user=request.user)

    if job.status != 'open':
        messages.error(request, "This job opening is currently closed for new applications.")
        return redirect('job_detail', job_id=job.id)

    # Prevent duplicate applications
    existing_application = Application.objects.filter(job=job, candidate=candidate).first()
    if existing_application:
        messages.warning(request, f"You have already applied for this job on {existing_application.applied_at.strftime('%b %d, %Y')}.")
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = candidate

            # Determine resume text to use for AI match score
            resume_text = candidate.extracted_resume_text
            candidate_skills = candidate.get_all_skills_list()

            # If user uploaded a specific resume for this application, extract text from it
            if application.resume_file:
                try:
                    custom_text = extract_text_from_pdf(application.resume_file.file)
                    if custom_text:
                        resume_text = custom_text
                        extracted_skills = extract_skills_from_text(custom_text)
                        candidate_skills = list(set(candidate_skills + extracted_skills))
                except Exception:
                    pass
            elif not application.resume_file and candidate.resume_file:
                # Copy profile resume
                application.resume_file = candidate.resume_file

            # Compute AI Resume-to-Job Match Score (Feature C)
            match_result = calculate_resume_job_match(resume_text, candidate_skills, job)
            application.match_score = match_result['score']
            application.matched_skills = ", ".join(match_result['matched_skills'])
            application.missing_skills = ", ".join(match_result['missing_skills'])
            application.similarity_explanation = match_result['explanation']
            application.status = 'applied'
            application.save()

            messages.success(
                request,
                f"Application submitted successfully! AI evaluated a {application.match_score:.1f}% match score based on your profile skills."
            )
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    context = {
        'job': job,
        'candidate': candidate,
        'form': form,
    }
    return render(request, 'applications/apply.html', context)


@login_required
@candidate_required
def my_applications(request):
    candidate = get_object_or_404(CandidateProfile, user=request.user)
    applications = Application.objects.filter(candidate=candidate).select_related('job', 'job__recruiter')

    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'applications': applications,
        'selected_status': status_filter,
    }
    return render(request, 'applications/my_applications.html', context)


@login_required
@recruiter_required
def update_application_status_ajax(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(Application, id=application_id, job__recruiter__user=request.user)
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            return JsonResponse({
                'success': True,
                'status': application.status,
                'status_display': application.get_status_display(),
                'badge_class': application.get_status_badge_class(),
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
