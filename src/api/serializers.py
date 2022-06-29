from rest_framework.serializers import ModelSerializer

from accounts.models import ForumUser
from music.models import ForumCategory, ForumComments, ForumPosted


class ForumUserSerializer(ModelSerializer):
    class Meta:
        model = ForumUser
        fields = ["first_name", "last_name", "email", "is_staff"]

    def get_first_name(self):
        print(self.initial_data.get("first_name"))
        return self.initial_data.get("last_name")


class ForumCommentsSerializer(ModelSerializer):
    class Meta:
        model = ForumComments
        fields = ("id", "text", "reply_to")


class ForumCategorySerializer(ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = ("id", "name", "description")


class ForumPostedSerializer(ModelSerializer):
    thread = ForumCommentsSerializer(many=True, read_only=True)
    posts = ForumCategorySerializer(read_only=True)

    class Meta:
        model = ForumPosted
        fields = ["id", "posts", "title", "description", "content", "thread"]


class PostsSerializer(ModelSerializer):
    thread = ForumCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = ForumPosted
        fields = ["id", "title", "description", "thread", "messages_count"]
