from rest_framework import serializers
from rateContent.models import TitleList, Platform, Review
# from rest_framework import validators

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('TitleList',)


class TitleListSerializer(serializers.ModelSerializer):

    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = TitleList
        fields = "__all__"


class PlatformSerializer(serializers.ModelSerializer):

    TitleList = TitleListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Platform
        fields = "__all__"

