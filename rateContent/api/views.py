from django.shortcuts import get_object_or_404
from rateContent.models import TitleList, Platform, Review
from rateContent.api.serializers import TitleListSerializer, PlatformSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rateContent.api.permissions import IsAdminORReadOnly, IsReviewerOrReadOnly

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rateContent.api.throttling import ReviewCreateThrottle, ReviewListThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rateContent.api.pagination import TitleListPagination , TitleListLFPagination, TitleListCPagination

# from rest_framework import mixins
from rest_framework import generics


class UserReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(reviewer_name__username=username)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Review.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(reviewer_name__username=username)
        return queryset


class TitleReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(TitleList=pk)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        show = TitleList.objects.get(pk=pk)
        username = self.request.user

        # Check if the user has already reviewed this title
        if Review.objects.filter(TitleList=show, reviewer_name=username).exists():
            raise ValidationError("Already reviewed this title")

        # Calculate the new average rating
        new_rating = serializer.validated_data['rating']
        if show.total_rating == 0:
            show.avg_rating = new_rating
        else:
            total_ratings = show.total_rating
            current_avg_rating = show.avg_rating
            show.avg_rating = ((current_avg_rating * total_ratings) + new_rating) / (total_ratings + 1)

        show.total_rating += 1
        show.save()

        serializer.save(TitleList=show, reviewer_name=username)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewerOrReadOnly]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "review-detail"


class ReviewList(generics.ListAPIView):
    """
    A simple ViewSet for viewing and editing accounts. 
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # throttle_classes = [ReviewListThrottle]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'reviewer_name__username']


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAdminORReadOnly]



class TitleListGV(generics.ListAPIView):
    queryset = TitleList.objects.all()
    serializer_class = TitleListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']

    pagination_class = TitleListCPagination

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']


class TitleListAV(APIView):

    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAdminORReadOnly]

    def get(self, request):
        movies = TitleList.objects.all()
        serializer = TitleListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TitleListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleListDetailAV(APIView):

    permission_classes = [IsAdminORReadOnly]

    def get(self, request, pk):
        try:
            movie = TitleList.objects.get(pk=pk)
            serializer = TitleListSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TitleList.DoesNotExist:
            return Response({'error': 'data does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            movie = TitleList.objects.get(pk=pk)
            serializer = TitleListSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TitleList.DoesNotExist:
            return Response({'error': 'data does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            movie = TitleList.objects.get(pk=pk)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TitleList.DoesNotExist:
            return Response({'error': 'data does not exist'}, status=status.HTTP_404_NOT_FOUND)


