from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Allergy, PreferredCuisine

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    allergies = serializers.ListField(
        child=serializers.CharField(max_length=10), required=False, write_only=True
    )
    preferred_cuisine = serializers.ListField(
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
            "preferred_cuisine",
            "diet",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"read_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_confirm", None)
        allergies_data = validated_data.pop("allergies", [])
        preferred_cuisine_data = validated_data.pop("preferred_cuisine", [])

        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()

        if allergies_data:
            # 존재하는 알러지만 가져오기
            existing_allergies = Allergy.objects.filter(ingredient__in=allergies_data)

            # 존재하는 알러지 목록을 집합으로 변환
            found_allergies = set(
                existing_allergies.values_list("ingredient", flat=True)
            )
            requested_allergies = set(allergies_data)

            # 존재하지 않는 알러지 찾기
            missing_allergies = requested_allergies - found_allergies

            # 존재하지 않는 알러지가 있으면 오류 반환
            if missing_allergies:
                raise serializers.ValidationError(
                    {"allergies": f"잘못된 알러지 입력: {', '.join(missing_allergies)}"}
                )

            # 유저의 알러지 설정
            instance.allergies.add(*existing_allergies)

        if preferred_cuisine_data:
            # 존재하는 음식만 가져오기
            existing_cuisines = PreferredCuisine.objects.filter(
                cuisine__in=preferred_cuisine_data
            )

            # 존재하는 음식을 집합으로 변환
            found_cuisines = set(existing_cuisines.values_list("cuisine", flat=True))
            requested_cuisines = set(preferred_cuisine_data)

            # 존재하지 않는 음식
            missing_cuisines = requested_cuisines - found_cuisines

            # 존재하지 않는 음식가 있으면 오류 반환
            if missing_cuisines:
                raise serializers.ValidationError(
                    {
                        "preferred_cuisine": f"잘못된 선호호음식 입력 :{', '.join(missing_cuisines)}"
                    }
                )

            # 유저의 선호음식
            instance.preferred_cuisine.add(*existing_cuisines)

        return instance

    # 출력 데이터를 보여주도록 변환
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["role"] = instance.get_role_display()

        representation["allergies"] = [
            allergy.ingredient for allergy in instance.allergies.all()
        ]
        representation["preferred_cuisine"] = [
            preferred_cuisine.cuisine
            for preferred_cuisine in instance.preferred_cuisine.all()
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


class PreferredCuisineSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreferredCuisine
        fields = ["id", "cuisine"]


class AllergySerializer(serializers.ModelSerializer):

    class Meta:
        model = Allergy
        fields = ["id", "ingredient"]


class ProfileUpdateSerializer(SignUpSerializer):

    class Meta(SignUpSerializer.Meta):
        fields = [
            "nickname",
            "age",
            "gender",
            "allergies",
            "preferred_cuisine",
            "diet",
            "profile_picture",
        ]
        extra_kwargs = {
            "nickname": {"required": False},
            "age": {"required": False},
            "gender": {"required": False},
        }

    # 변경 데이터로 업데이트
    def update(self, instance, validated_data):
        if "allergies" in validated_data:
            allergy_names = validated_data.pop("allergies", [])

            # 존재하는 알러지만 가져오기
            existing_allergies = Allergy.objects.filter(ingredient__in=allergy_names)
            found_allergies = set(
                existing_allergies.values_list("ingredient", flat=True)
            )
            requested_allergies = set(allergy_names)

            # 존재하지 않는 알러지 찾기
            missing_allergies = requested_allergies - found_allergies

            # 만약 존재하지 않는 알러지가 있다면, 오류 반환
            if missing_allergies:
                raise serializers.ValidationError(
                    {
                        "allergies": f"목록에 없는 알러지를 입력: {','.join(missing_allergies)}"
                    }
                )
            # 기존 알러지를 새로운 값으로 교체
            instance.allergies.set(existing_allergies)

        if "preferred_cuisine" in validated_data:
            cuisine_names = validated_data.pop("preferred_cuisine", [])

            # 존재하는 음식만 가져오기
            existing_cuisines = PreferredCuisine.objects.filter(
                cuisine__in=cuisine_names
            )
            found_cuisines = set(existing_cuisines.values_list("cuisine", flat=True))
            requested_cuisines = set(cuisine_names)

            # 존재하지 않는 값 확인
            missing_cuisines = requested_cuisines - found_cuisines
            if missing_cuisines:
                raise serializers.ValidationError(
                    {
                        "preferred_cuisine": f"잘못된 선호음식 입력: {','.join(missing_cuisines)}"
                    }
                )

            # 기존 값 대체
            instance.preferred_cuisine.set(existing_cuisines)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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


class UserSerializer(serializers.ModelSerializer):
    allergies = serializers.SerializerMethodField()
    preferred_cuisine = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nickname",
            "age",
            "gender",
            "allergies",
            "preferred_cuisine",
            "diet",
            "profile_picture",
        ]

    def get_allergies(self, obj):
        return obj.allergies.values_list("ingredient", flat=True)

    def get_preferred_cuisine(self, obj):
        return obj.preferred_cuisine.values_list("cuisine", flat=True)
