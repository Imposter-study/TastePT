from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Allergy

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    allergies = serializers.ListField(
        child=serializers.CharField(max_length=10), required=False, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "nickname",
            "role",
            "age",
            "gender",
            "allergies",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"read_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_confirm", None)
        allergies_data = validated_data.pop("allergies", [])

        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()

        if allergies_data:
            for allergy_name in allergies_data:
                allergy, created = Allergy.objects.get_or_create(
                    Ingredient=allergy_name
                )
                instance.allergies.add(allergy)

        return instance

    # 출력 데이터를 보여주도록 변환
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["role"] = instance.get_role_display()

        representation["allergies"] = [
            allergy.Ingredient for allergy in instance.allergies.all()
        ]

        return representation

    # 닉네임 검증
    def validate_nickname(self, value):
        if len(value) > 30:
            raise serializers.ValidationError("닉네임은 30글자 이하이어야 합니다.")
        return value

    # 비밀번호 검증
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        return value

    # 비밀번호 확인 및 일치 여부 검증
    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "비밀번호가 일치하지 않습니다."}
            )

        return data


class ProfileUpdateSerializer(SignUpSerializer):
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta(SignUpSerializer.Meta):
        fields = [
            "nickname",
            "age",
            "gender",
        ]
        extra_kwargs = {
            "nickname": {"required": False},
            "age": {"required": False},
            "gender": {"required": False},
        }

    # 변경 데이터로 업데이트
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    # 비밀번호 일치 여부 검증 코드 삭제
    def validate(self, data):
        return data


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 일치하지 않습니다.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        return value

    def validate(self, data):
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        new_password_confirm = data.get("new_password_confirm")

        if old_password == new_password:
            raise serializers.ValidationError(
                {"password_confirm": "이전 비밀번호와 현재 비밀번호가 같습니다."}
            )

        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "비밀번호가 일치하지 않습니다."}
            )

        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
