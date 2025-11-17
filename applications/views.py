from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import JobApplication
from .serializers import JobApplicationSerializer, JobApplicationCreateSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class JobApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only the logged-in user's applications"""
        user = self.request.user
        queryset = JobApplication.objects.filter(user=user)
        
        # Filter by status if provided
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(company_name__icontains=search) | 
                Q(job_title__icontains=search)
            )
        
        return queryset
    
    def get_serializer_class(self):
        """Use different serializer for create/update"""
        if self.action in ['create', 'update', 'partial_update']:
            return JobApplicationCreateSerializer
        return JobApplicationSerializer
    
    def perform_create(self, serializer):
        """Automatically set the user when creating"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get statistics dashboard data"""
        user = request.user
        applications = JobApplication.objects.filter(user=user)
        
        stats = {
            'total': applications.count(),
            'applied': applications.filter(status='applied').count(),
            'interview_scheduled': applications.filter(status='interview_scheduled').count(),
            'technical_round': applications.filter(status='technical_round').count(),
            'hr_round': applications.filter(status='hr_round').count(),
            'offer_received': applications.filter(status='offer_received').count(),
            'rejected': applications.filter(status='rejected').count(),
        }
        
        return Response(stats)
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Anyone can register (no login required)
    serializer_class = RegisterSerializer
