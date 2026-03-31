from django.urls import path
from .views import (
    CandidateListCreateView,
    JobListCreateView,
    JobRecommendationView,
    CandidateRecommendationView,
)

urlpatterns = [
    path('candidates/', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('candidates/<int:candidate_id>/recommend-jobs/', JobRecommendationView.as_view(), name='recommend-jobs'),
    path('jobs/<int:job_id>/recommend-candidates/', CandidateRecommendationView.as_view(), name='recommend-candidates'),
]