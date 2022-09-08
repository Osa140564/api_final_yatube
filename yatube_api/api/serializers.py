from rest_framework import serializers

from posts.models import Comment, Group, Post, Follow, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'post', 'created')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('author',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username'
                                          )

    class Meta:
        model = Post
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Уже подписаны'
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        return data
