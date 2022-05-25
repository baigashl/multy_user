from organizations.models import OrganizationUser, Organization, OrganizationOwner
from rest_framework.reverse import reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from accounts.accounts_nested.serializers import AccountInlineSerializers
from accounts.models import Account
from users.models import CustomUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    user_organizations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'url',
            'email',
            'full_name',
            'user_organizations'
        ]
        read_only_fields = ['user_organizations']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("user-detail", kwargs={"pk": obj.id}, request=request)

    def get_user_organizations(self, obj):
        qs = Organization.objects.filter(
            users=obj.id
        )
        return AccountInlineSerializers(qs, many=True).data


class UserWishListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    wishlist = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'url',
            'email',
            'full_name',
            'wishlist'
        ]
        read_only_fields = ['user_organizations']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("user-detail", kwargs={"pk": obj.id}, request=request)

    def get_wishlist(self, obj):
        qs = Account.objects.filter(
            users_wishlist=obj
        )
        return AccountInlineSerializers(qs, many=True).data


class UserAccountSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'url',
            'email',
            'full_name',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("user-detail", kwargs={"pk": obj.id}, request=request)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs


class RegisterOrgUserSerializers(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = ['id', 'url', 'user', 'organization']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(
            full_name=user_data['full_name'],
            email=user_data['email'],
            password=user_data['password']
        )
        user.set_password(user_data['password'])
        organization_user = OrganizationUser.objects.create(
            user=user,
            organization=validated_data['organization']
        )
        return organization_user

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("org_user-detail", kwargs={"pk": obj.id}, request=request)


class OrgUserDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    organization = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationUser
        fields = [
            'id',
            'url',
            'user',
            'organization'
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("org_user-detail", kwargs={"pk": obj.id}, request=request)

    def get_organization(self, obj):
        qs = Organization.objects.filter(
            organization_users=obj.id
        )
        return AccountInlineSerializers(qs, many=True).data


class OrgUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = [
            'user',
            'organization'
        ]
        read_only_fields = ['user']








