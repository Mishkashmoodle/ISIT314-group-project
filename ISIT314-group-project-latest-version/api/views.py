# ================= views.py (Class-Based Views) =================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, Job
from .serializers import CandidateSerializer, JobSerializer
from .services import MatchingService
from difflib import SequenceMatcher

def fuzzy_match(keyword, text):
    if not keyword or not text:
        return False

    keyword = keyword.lower().strip()
    text = text.lower().strip()

    if keyword in text:
        return True

    words = text.split()

    for word in words:
        similarity = SequenceMatcher(None, keyword, word).ratio()
        if similarity >= 0.75:
            return True

    return False

# Candidate Views
class CandidateListCreateView(APIView):

        def get(self, request):
            keyword = request.GET.get('keyword')
            skill = request.GET.get('skill')
            education = request.GET.get('education')
            experience = request.GET.get('experience')
            location = request.GET.get('location')
            mode = request.GET.get('mode')

            candidates = Candidate.objects.all()

            if keyword:
                candidates = candidates.filter(
                    name__icontains=keyword
                ) | candidates.filter(
                    contact__icontains=keyword
                ) | candidates.filter(
                    education__icontains=keyword
                ) | candidates.filter(
                    major__icontains=keyword
                ) | candidates.filter(
                    preferred_location__icontains=keyword
                )

            if skill:
                candidates = candidates.filter(skills__contains=[skill])

            if education:
                candidates = candidates.filter(education__iexact=education)

            if experience:
                candidates = candidates.filter(experience__gte=experience)

            if location:
                candidates = candidates.filter(preferred_location__icontains=location)

            if mode:
                candidates = candidates.filter(preferred_working_mode__iexact=mode)

            if keyword:
                candidates = [
                    candidate for candidate in candidates
                    if fuzzy_match(keyword, candidate.name)
                    or fuzzy_match(keyword, candidate.contact)
                    or fuzzy_match(keyword, candidate.education)
                    or fuzzy_match(keyword, candidate.major)
                    or fuzzy_match(keyword, candidate.preferred_location)
                    or any(fuzzy_match(keyword, skill) for skill in candidate.skills)
                ]

            serializer = CandidateSerializer(candidates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        def post(self, request):
            serializer = CandidateSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListCreateView(APIView):

        def get(self, request):
            keyword = request.GET.get('keyword')
            mode = request.GET.get('mode')
            location = request.GET.get('location')
            education = request.GET.get('education')
            experience = request.GET.get('experience')
            skill = request.GET.get('skill')

            jobs = Job.objects.all()

            if keyword:
                jobs = jobs.filter(
                    title__icontains=keyword
                ) | jobs.filter(
                    company__icontains=keyword
                ) | jobs.filter(
                    description__icontains=keyword
                ) | jobs.filter(
                    education__icontains=keyword
                ) | jobs.filter(
                    location__icontains=keyword
                )

            if mode:
                jobs = jobs.filter(mode__iexact=mode)

            if location:
                jobs = jobs.filter(location__icontains=location)

            if education:
                jobs = jobs.filter(education__iexact=education)

            if experience:
                jobs = jobs.filter(experience__lte=experience)

            if skill:
                jobs = jobs.filter(skills__contains=[skill])

            if keyword:
                jobs = [
                    job for job in jobs
                    if fuzzy_match(keyword, job.title)
                    or fuzzy_match(keyword, job.company)
                    or fuzzy_match(keyword, job.description)
                    or fuzzy_match(keyword, job.education)
                    or fuzzy_match(keyword, job.location)
                    or any(fuzzy_match(keyword, skill) for skill in job.skills)
                ]

            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        def post(self, request):
            serializer = JobSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Job Views
class JobRecommendationView(APIView):

    def get(self, request, candidate_id):
        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response(
                {"error": "Candidate not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        jobs = Job.objects.all()
        matcher = MatchingService()
        recommendations = matcher.recommend_jobs(candidate, jobs)

        response_data = []
        for item in recommendations:
            response_data.append({
                "job": JobSerializer(item["job"]).data,
                "score": item["score"]
            })

        return Response(response_data, status=status.HTTP_200_OK)


# Recommendation Views
class CandidateRecommendationView(APIView):

    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found."},
                status=status.HTTP_404_NOT_FOUND   
            )
        
        candidates = Candidate.objects.all()
        matcher = MatchingService()
        recommendations = matcher.recommend_candidates(job, candidates)

        response_data = []
        for item in recommendations:
            response_data.append({
                "candidate": CandidateSerializer(item['candidate']).data,
                "score": item['score']
            })

        return Response(response_data, status=status.HTTP_200_OK)
    
