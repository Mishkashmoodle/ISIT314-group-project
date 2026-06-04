# ================= views.py (Class-Based Views) =================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, Job, Business, Account, SavedJob, Match
from .serializers import CandidateSerializer, JobSerializer, BusinessSerializer, AccountSerializer, SavedJobSerializer, MatchSerializer
from .services import MatchingService
from difflib import SequenceMatcher
from .resume_parser import parse_resume

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

class CandidateDetailView(APIView):

    def get(self, request, candidate_id):
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Candidate.DoesNotExist:
            return Response(
                {"error": "Candidate not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, candidate_id):
        try:
            candidate = Candidate.objects.get(id=candidate_id)

            data = request.data.copy()

            if "resume" in request.FILES:
                data["resume"] = request.FILES["resume"]

            serializer = CandidateSerializer(
                candidate,
                data=data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Candidate.DoesNotExist:
            return Response(
                {"error": "Candidate not found."},
                status=status.HTTP_404_NOT_FOUND
            )


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
        
class BusinessListCreateView(APIView):

    def get(self, request):
        businesses = Business.objects.all()
        serializer = BusinessSerializer(businesses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BusinessSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessDetailView(APIView):

    def get(self, request, business_id):
        try:
            business = Business.objects.get(id=business_id)
            serializer = BusinessSerializer(business)
            return Response(serializer.data)

        except Business.DoesNotExist:
            return Response(
                {"error": "Business not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, business_id):
        try:
            business = Business.objects.get(id=business_id)

            serializer = BusinessSerializer(
                business,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Business.DoesNotExist:
            return Response(
                {"error": "Business not found."},
                status=status.HTTP_404_NOT_FOUND
            )

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
    

class ResumeParseView(APIView):
    
    def post(self, request):
        resume_file = request.FILES.get("resume")

        if not resume_file:
            return Response(
                {"error": "No resume file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            parsed_data = parse_resume(resume_file)
            return Response(parsed_data, status=status.HTTP_200_OK)

        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            return Response(
                {"error": "Could not parse resume."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class AccountRegisterView(APIView):

    def post(self, request):
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavedJobCreateView(APIView):

    def post(self, request):
        serializer = SavedJobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateSavedJobsView(APIView):

    def get(self, request, candidate_id):
        saved_jobs = SavedJob.objects.filter(candidate_id=candidate_id)
        serializer = SavedJobSerializer(saved_jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AccountLoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            account = Account.objects.get(email=email, password=password)

            response_data = {
                "id": account.id,
                "email": account.email,
                "account_type": account.account_type
            }

            if account.account_type == "candidate":
                candidate = Candidate.objects.filter(account=account).first()

                if candidate:
                    response_data["candidate_id"] = candidate.id

            if account.account_type == "business":
                business = Business.objects.filter(account=account).first()

                if business:
                    response_data["business_id"] = business.id

            return Response(response_data, status=status.HTTP_200_OK)

        except Account.DoesNotExist:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST
            )

class MatchCreateView(APIView):

    def post(self, request):
        serializer = MatchSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessMatchesView(APIView):

    def get(self, request, business_id):
        matches = Match.objects.filter(business_id=business_id)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MatchDetailView(APIView):

    def patch(self, request, match_id):
        try:
            match = Match.objects.get(id=match_id)

            serializer = MatchSerializer(
                match,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Match.DoesNotExist:
            return Response(
                {"error": "Match not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    def delete(self, request, match_id):
        try:
            match = Match.objects.get(id=match_id)
            match.delete()

            return Response(
                {"message": "Match removed."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Match.DoesNotExist:
            return Response(
                {"error": "Match not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class JobDetailView(APIView):

    def delete(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            job.delete()

            return Response(
                {"message": "Job removed."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found."},
                status=status.HTTP_404_NOT_FOUND
            )