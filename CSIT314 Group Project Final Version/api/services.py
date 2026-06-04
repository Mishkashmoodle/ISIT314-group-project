# ================= services.py =================

class MatchingService:
    def __init__(self, candidate=None, job=None):
        self.candidate = candidate
        self.job = job

    def calculate_score(self, candidate, job):
        score = 0

        if candidate.education == job.education:
            score += 1

        score += len(set(candidate.skills) & set(job.skills))

        score += max(0, 5 - abs(candidate.experience - job.experience))

        if candidate.preferred_working_mode == job.mode:
            score += 1

        if candidate.preferred_location.lower() == job.location.lower():
            score += 1

        return score

    def recommend_jobs(self, candidate, jobs):
        ranked = sorted([
            {"job": job, "score": self.calculate_score(candidate, job)}
            for job in jobs
        ], key=lambda x: x["score"], reverse=True)

        if candidate.membership:
            return ranked

        return ranked[:10]

    def recommend_candidates(self, job, candidates):
        ranked = sorted([
            {
                "candidate": candidate,
                "score": self.calculate_score(candidate, job)
            }
            for candidate in candidates
        ], key=lambda x: x["score"], reverse=True)

        if job.business and job.business.membership:
            return ranked

        return ranked[:10]