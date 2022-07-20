from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import ForumUser
from api.serializers import (ForumCategorySerializer, ForumPostedSerializer,
                             ForumUserSerializer, PostsSerializer)
from music.models import ForumCategory, ForumPosted


class UserViewSet(ModelViewSet):
    queryset = ForumUser.objects.all()
    serializer_class = ForumUserSerializer


class PostListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ForumPosted.objects.all()
    serializer_class = PostsSerializer


class CategoryCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForumCategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = ForumCategory.objects.all()
    serializer_class = ForumCategorySerializer

    def get_object(self):

        return ForumCategory.objects.get(
            id=self.kwargs.get("pk"),
        )


class CategoryUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForumCategorySerializer

    def put(self, request, *args, **kwargs):
        cat_id = kwargs.get("pk")
        category = get_object_or_404(ForumCategory, id=cat_id)
        serializer = ForumCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForumUserSerializer
    queryset = ForumCategory.objects.all()

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        self.perform_destroy(category)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostDetailView(RetrieveAPIView):
    queryset = ForumPosted.objects.all()
    serializer_class = ForumPostedSerializer

    def get_object(self):

        return ForumPosted.objects.get(
            uuid=self.kwargs.get("uuid"),
        )
