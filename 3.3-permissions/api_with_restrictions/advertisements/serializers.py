from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "description",
            "creator",
            "status",
            "created_at",
        )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user = self.context["request"].user
        open_count = Advertisement.objects.filter(
            creator=user, status=AdvertisementStatusChoices.OPEN
        ).count()

        if self.instance is None:
            if open_count >= 10:
                raise serializers.ValidationError(
                    {"status": "У вас не может быть более 10 открытых объявлений."}
                )

        return data


class FavoriteDetailSerializer(serializers.ModelSerializer):
    """Serializer для представления деталей объекта Избранное."""

    advertisement = AdvertisementSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["user", "advertisement"]
        read_only_fields = ["user"]


class FavoriteCreateSerializer(serializers.ModelSerializer):
    """Serializer для создания объекта Избранное."""

    advertisement = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ["advertisement"]

    def create(self, validated_data):
        validated_data["user"] = self.context[
            "request"
        ].user
        return super().create(validated_data)