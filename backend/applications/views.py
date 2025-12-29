import requests
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Application
from .serializers import ApplicationSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Application.objects.filter(user=self.request.user)

        status = self.request.query_params.get("status")
        company = self.request.query_params.get("company")
        sort_by = self.request.query_params.get("sort")

        if status:
            queryset = queryset.filter(status=status)

        if company:
            queryset = queryset.filter(company_name__icontains=company)

        if sort_by in ["deadline", "applied_date"]:
            queryset = queryset.order_by(sort_by)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    total = Application.objects.filter(user=user).count()
    status_counts = (
        Application.objects.filter(user=user)
        .values("status")
        .annotate(count=models.Count("status"))
    )

    return Response({
        "total_applications": total,
        "status_breakdown": status_counts
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def predict_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    payload = {
        "cpi": request.data["cpi"],
        "skills": request.data["skills"],
        "projects": request.data["projects"],
        "experience_months": request.data["experience_months"],
        "college_tier": request.data["college_tier"],
        "role_type": application.role_type,
        "company_type": application.company_type
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=payload,
            timeout=5
        )
        response.raise_for_status()

        probability = response.json()["shortlisting_probability"]
        application.prediction_score = probability
        application.save()

        return Response({
            "application_id": application.id,
            "prediction_score": probability
        })

    except requests.exceptions.RequestException:
        return Response(
            {"error": "ML service unavailable"},
            status=503
        )
