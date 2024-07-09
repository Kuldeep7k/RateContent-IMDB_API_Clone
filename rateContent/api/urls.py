from django.urls import path, include
from rateContent.api.views import (TitleListDetailAV, TitleListAV,PlatformViewSet, TitleReviewList, ReviewList,
                                    ReviewDetail, ReviewCreate, UserReviewList, TitleListGV)
# from rateContent.api.views import moviesList, movieDetails
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('platforms', PlatformViewSet, basename='platformView')

urlpatterns = [
    path('titles/', TitleListAV.as_view(), name="titles-list"),

    path('newtitles/', TitleListGV.as_view(), name="newtitles-list"),

    path('titles/<int:pk>/', TitleListDetailAV.as_view(), name="title-detail"),

    path('', include(router.urls)),

    # path('platforms/', PlatformAV.as_view(), name="platform-list"),
    # path('platforms/<int:pk>/', PlatformDetailAV.as_view(), name="platform-detail"),


    # path('reviews/<int:pk>', ReviewDetail.as_view(),name="review-list"),

    path('reviews/', ReviewList.as_view(), name="review-list"),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),

    # path('reviews/<str:username>/', UserReviewList.as_view(), name="user-reviews-list"),
    path('reviews/username/', UserReviewList.as_view(), name="user-reviews-list"),

    path('title/<int:pk>/review-create/',
         ReviewCreate.as_view(), name="review-create"),
    path('title/<int:pk>/reviews/',
         TitleReviewList.as_view(), name="title-reviews"),
]
