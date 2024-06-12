from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from Admin.models import Comment
from Admin.Serializers import comment_serializer
from Admin.utils import DefPagination

class Comments(viewsets.GenericViewSet, generics.mixins.ListModelMixin, generics.mixins.RetrieveModelMixin, generics.mixins.UpdateModelMixin, generics.mixins.DestroyModelMixin):

    serializer_class = comment_serializer.CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = DefPagination
    # permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=False, methods=['get'], url_path='flagged', url_name='flagged')
    def get_all_flagged(self, request):

        try:
            flagged = Comment.objects.filter(is_flagged = True)
            comments = self.get_serializer(flagged, many = True).data

            return Response({
                'FLAGGED': comments
            })
                
        except Exception as e:
            return Response({
            'ERROR': 'REQUEST NOT EXECUTED',
            'DETAIL': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)