from rest_framework import serializers

from .models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    subpassword = serializers.CharField(required=True, label='校验密码', write_only=True,)

    class Meta:
        model = MyUser
        fields = ('username', 'password', 'email', 'subpassword')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def validate(self, data):
        subpassword = data.get('subpassword')
        password = data.get('password')
        if not (subpassword == password):
            raise serializers.ValidationError('两次输入的密码不一致, 请重试')

        return data

    def create(self, validated_data):
        del validated_data["subpassword"]
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, label='旧密码', write_only=True)
    new_subpassword = serializers.CharField(required=True, label='校验密码', write_only=True)

    class Meta:
        model = MyUser
        fields = ('old_password', 'new_subpassword', 'password', 'username', 'email')
        read_only_fields = ['username', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def validate(self, data):
        new_subpassword = data.get('new_subpassword')
        password = data.get('password')
        if not (new_subpassword == password):
            raise serializers.ValidationError('两次输入的密码不一致, 请重试')

        return data

    def update(self, instance, validated_data):
        old_password = validated_data['old_password']
        password = validated_data['password']

        if not instance.check_password(old_password):
            raise serializers.ValidationError('旧密码填写错误')

        instance.set_password(password)
        instance.save()
        return instance
