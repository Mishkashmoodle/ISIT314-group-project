# ================= serializers.py =================
from rest_framework import serializers
from .models import Candidate, Job

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    REQUIRED_FIELDS = {
        'title': 'Job title is required.',
        'company': 'Company information is required.',
        'description': 'Job description is required.',
        'education': 'Required education level is required.',
        'skills': 'Required skills are required.',
        'experience': 'Years of experience is required.',
        'mode': 'Work mode is required.',
        'location': 'Job location is required.',
    }

    class Meta:
        model = Job
        fields = '__all__'

    def validate(self, attrs):
        errors = {}

        for field_name, message in self.REQUIRED_FIELDS.items():
            value = attrs.get(field_name)

            if value is None:
                errors[field_name] = message
                continue

            if isinstance(value, str) and not value.strip():
                errors[field_name] = message
                continue

            if field_name == 'skills' and (not isinstance(value, list) or not value):
                errors[field_name] = 'Provide at least one required skill.'
                continue

        if 'experience' in attrs and attrs['experience'] is not None and attrs['experience'] < 0:
            errors['experience'] = 'Years of experience cannot be negative.'

        if 'mode' in attrs and isinstance(attrs['mode'], str):
            normalized_mode = attrs['mode'].strip()
            allowed_modes = {'Remote', 'On-site', 'Hybrid'}
            if normalized_mode not in allowed_modes:
                errors['mode'] = 'Work mode must be Remote, On-site, or Hybrid.'
            else:
                attrs['mode'] = normalized_mode

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
