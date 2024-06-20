from rest_framework import serializers
from . models import User, Hostel, Block, Room, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "approved", "is_superuser"]
        extra_kwargs = {
            "password": {"write_only": True}, 
            "approved": {"read_only": True},
            "is_superuser": {"read_only": True},
            }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ["id", "name", "secret_key"]
        extra_kargs = {"secret_key": {"read_only": True}}

class BlockSerializer(serializers.ModelSerializer):
    room_count = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    hostel_id = serializers.SerializerMethodField()

    class Meta:
        model = Block
        fields = ["id", "name", "room_count", "hostel", "hostel_id"]

    def get_room_count(self, obj):
        return obj.room_set.count()

    def get_hostel_id(self, obj):
        return obj.room_set.count()
    
    def get_hostel(self, obj):
        return obj.hostel.name

class RoomSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    filled_up = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    block = serializers.SerializerMethodField()
    block_id = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["id", "name", "student_count", "filled_up", "hostel", "block", "block_id", "capacity"]

    def get_student_count(self, obj):
        return obj.student_set.count()
    
    def get_hostel(self, obj):
        return obj.block.hostel.name
    
    def get_block(self, obj):
        return obj.block.name
    
    def get_block_id(self, obj):
        return obj.block.id
    
    def get_filled_up(self, obj):
        if obj.student_set.count() == obj.capacity:
            return True
        else:
            return False

class StudentSerializer(serializers.ModelSerializer):
    room_id = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ["id", "name", "matric_no", "college", "department", "student_no", "parent_no", "resumption_date", "room_id"]

    def get_room_id(self, obj):
        return obj.room.id