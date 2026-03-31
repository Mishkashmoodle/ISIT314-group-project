# ================= views.py (Class-Based Views) =================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, Job
from .serializers import CandidateSerializer, JobSerializer
from .services import MatchingService

# Candidate Views
class CandidateListCreateView(APIView):

    def get(self, request):
        skill = request.GET.get('skill')
        education = request.GET.get('education')

        candidates = Candidate.objects.all()

        if skill:
            candidates = candidates.filter(skills__contains=[skill])
        if education:
            candidates = candidates.filter(education=education)

        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

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

        jobs = Job.objects.all()

        if keyword:
            jobs = jobs.filter(description__icontains=keyword)
        if mode:
            jobs = jobs.filter(mode__iexact=mode)
        if location:
            jobs = jobs.filter(location__iexact=location)

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

        return Response(response_data, status)
    