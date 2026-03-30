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

        return score

    def recommend_jobs(self, candidate, jobs, top_k=10):
        ranked = sorted([
            {"job": job, "score": self.calculate_score(candidate, job)}
            for job in jobs
        ], key=lambda x: x['score'], reverse=True)

        return ranked[:top_k]

    def recommend_candidates(self, job, candidates, top_k=10):
        ranked = sorted([
            {"candidate": c, "score": self.calculate_score(c, job)}
            for c in candidates
        ], key=lambda x: x['score'], reverse=True)

        return ranked[:top_k]