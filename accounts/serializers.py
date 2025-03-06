from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

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
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"read_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_confirm", None)

        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    # 출력 데이터를 보여주도록 변환
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["role"] = instance.get_role_display()
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
