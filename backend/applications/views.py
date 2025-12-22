from django.db import models
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Application.objects.filter(user=self.request.user)

        status = self.request.query_params.get('status')
        company = self.request.query_params.get('company')
        sort_by = self.request.query_params.get('sort')

        if status:
            queryset = queryset.filter(status=status)

        if company:
            queryset = queryset.filter(company_name__icontains=company)

        if sort_by in ['deadline', 'applied_date']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    total = Application.objects.filter(user=user).count()

    status_counts = Application.objects.filter(user=user).values('status').annotate(count=models.Count('status'))

    return Response({
        "total_applications": total,
        "status_breakdown": status_counts
    })