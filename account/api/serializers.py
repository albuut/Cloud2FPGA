from rest_framework import serializers

from account.models import User
from games.models import Games

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type":'password'}, write_only=True)

    class Meta:
        model = User
        fields =    ['email','username','password','password2']
        extra_kwargs = {
                'password': {'write_only': True}
        }

    def save(self):
        account = User(
                    email=self.validated_data['email'],
                    username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class UserGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['account_id','username','game']
        depth = 1 #to get nested data


class UserSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['account_id','play_flag','sync_flag','sync_done_flag','updated','current_storage','total_storage']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['game_name','game_file_link','file_location','game_year','cover','file_size','rma_file','rbf_file','game_type','manufacturer','category']



class UserStorageInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['current_storage','total_storage']
        depth = 1 #to get nested data