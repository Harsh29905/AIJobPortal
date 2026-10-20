from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import candidate_required
from candidates.models import CandidateProfile
from .services import get_job_recommendations_for_candidate


@login_required
@candidate_required
def recommendations_list(request):
    candidate = get_object_or_404(CandidateProfile, user=request.user)
    recommendations = get_job_recommendations_for_candidate(candidate, limit=20)

    context = {
        'candidate': candidate,
        'recommendations': recommendations,
        'candidate_skills': candidate.get_all_skills_list(),
    }
    return render(request, 'recommendations/recommendations_list.html', context)
