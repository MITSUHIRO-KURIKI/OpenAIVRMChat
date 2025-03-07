# https://www.django-rest-framework.org/api-guide/status-codes/
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.utils import StandardThrottle
from apps.user_properties.models import UserProfile
from ..serializers import UserProfileSerializer


class UserProfileViewSet(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes   = [StandardThrottle]

    def get(self, request, *args, **kwargs):
        try:
            user_profile_obj = get_object_or_404(UserProfile,
                                                 unique_account_id = request.user,)

            serializer = UserProfileSerializer(instance=user_profile_obj)
            response   = Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = Response({
                'message': 'failed',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response

    def patch(self, request, *args, **kwargs):
        try:
            user_profile_obj = get_object_or_404(UserProfile,
                                                 unique_account_id = request.user,)
            if user_profile_obj:
                serializer = UserProfileSerializer(instance=user_profile_obj, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response = Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response = Response({}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response = Response({
                'message': 'failed',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response