from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import candidate_required
from .models import CandidateProfile
from .forms import CandidateProfileForm, ResumeUploadForm
from applications.models import Application
from recommendations.services import (
    extract_text_from_pdf,
    extract_skills_from_text,
    get_job_recommendations_for_candidate,
)
from recommendations.models import JobRecommendation


@login_required
@candidate_required
def candidate_dashboard(request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    recent_applications = Application.objects.filter(candidate=profile).select_related('job', 'job__recruiter')[:5]
    
    # Calculate statistics
    total_applied = Application.objects.filter(candidate=profile).count()
    shortlisted_count = Application.objects.filter(candidate=profile, status__in=['shortlisted', 'interview', 'hired']).count()
    
    # AI Recommended jobs
    recommended_jobs = get_job_recommendations_for_candidate(profile, limit=6)

    context = {
        'profile': profile,
        'recent_applications': recent_applications,
        'total_applied': total_applied,
        'shortlisted_count': shortlisted_count,
        'recommended_jobs': recommended_jobs,
        'completion_pct': profile.profile_completion_percentage(),
    }
    return render(request, 'candidates/dashboard.html', context)


@login_required
@candidate_required
def candidate_profile_edit(request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('candidate_dashboard')
    else:
        form = CandidateProfileForm(instance=profile)
    return render(request, 'candidates/profile_edit.html', {'form': form, 'profile': profile})


@login_required
@candidate_required
def candidate_resume_upload(request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            saved_profile = form.save()
            # AI Feature A: Resume Skill Extraction
            if saved_profile.resume_file:
                try:
                    resume_text = extract_text_from_pdf(saved_profile.resume_file.path)
                    saved_profile.extracted_resume_text = resume_text
                    extracted_skills = extract_skills_from_text(resume_text)
                    saved_profile.extracted_skills = ", ".join(extracted_skills)
                    saved_profile.save()
                    messages.success(
                        request,
                        f"Resume processed successfully! AI extracted {len(extracted_skills)} technical and professional skills."
                    )
                except Exception as e:
                    messages.warning(
                        request,
                        "Resume uploaded, but automatic skill extraction encountered an issue. You can still enter skills manually."
                    )
            return redirect('candidate_dashboard')
        else:
            messages.error(request, "Failed to upload resume. Please check the file format.")
    else:
        form = ResumeUploadForm(instance=profile)
    return render(request, 'candidates/resume_upload.html', {'form': form, 'profile': profile})
