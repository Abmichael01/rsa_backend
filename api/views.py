from django.shortcuts import render
from . serializers import UserSerializer, HostelSerializer, BlockSerializer, RoomSerializer, StudentSerializer
from . models import User, Hostel, Block, Room, Student
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import json



# Create your views here.
class UserCreationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(approved=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_hostel(request):
    data = json.loads(request.body)
    name = data["name"]
    secret_key = data["secretKey"]
    new_hostel = Hostel.objects.create(name=name, secret_key=secret_key)
    new_hostel.save()
    hostels = Hostel.objects.all()
    
    serializer = HostelSerializer(hostels, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_hostels(request):
    hostels = Hostel.objects.all()
    serializer = HostelSerializer(hostels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_hostel(request, pk):
    hostel = Hostel.objects.get(id=pk)
    serializer = HostelSerializer(hostel, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def access_hostel(request):
    data = json.loads(request.body)
    hostel_id = data["hostelId"]
    secret_key = data["secretKey"]
    hostel = Hostel.objects.filter(id=hostel_id, secret_key=secret_key).first()
    allow = False
    if hostel:
        allow = True
        return Response({"allow": allow}, status=status.HTTP_200_OK)
    else:
        allow = False
        return Response({"not_allowed": allow}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_block(request):
    data = json.loads(request.body)
    hostel_id = data["hostelId"]
    block_name = data["blockName"]
    room_no = int(data["roomNo"])
    capacity = int(data["capacity"])
    hostel = Hostel.objects.filter(id=hostel_id).first()
    print(data)
    if hostel:
        new_block = hostel.block_set.create(name=block_name)
        new_block.save()

        for i in range(1, room_no+1):
            room_name = f"Room {i}"
            new_room = new_block.room_set.create(name=room_name, capacity=capacity)
            new_room.save()

        blocks = hostel.block_set.all()

        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_blocks(request, pk):
    hostel_id = pk
    hostel = Hostel.objects.filter(id=hostel_id).first()
    if hostel:
        blocks = hostel.block_set.all()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_rooms(request, pk):
    block = Block.objects.get(id=pk)
    rooms = block.room_set.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_block(request, pk):
    block = Block.objects.get(id=pk)
    serializer = BlockSerializer(block, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_student(request):
    data = json.loads(request.body)
    room_id = data["roomId"]
    name = data["studentName"]
    matric_no = data["matricNo"]
    college = data["college"]
    department = data["department"]
    student_no = data["studentNo"]
    parent_no = data["parentNo"]
    resumption_date= data["resumptionDate"]

    room = Room.objects.get(id=room_id)
    if room:
        new_student = Student.objects.create(
            name = name,
            matric_no = matric_no,
            college = college,
            department = department,
            student_no = student_no,
            parent_no = parent_no,
            resumption_date = resumption_date,
            room = room,
        )
        new_student.save()

        return Response({"message": "added"}, status=status.HTTP_201_CREATED)
    return Response({"message": "room not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_room(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_students(request, pk):
    room = Room.objects.get(id=pk)
    students = room.student_set.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_hostel_data(request, pk):
    hostel = Hostel.objects.get(id=pk)
    blocks = hostel.block_set.all()
    rooms = Room.objects.filter(block__in=blocks)
    students = Student.objects.filter(room__in=rooms)

    hostel_serializer = HostelSerializer(hostel, many=False)
    block_serializer = BlockSerializer(blocks, many=True)
    room_serializer = RoomSerializer(rooms, many=True)
    student_serializer = StudentSerializer(students, many=True)

    data = {
        "hostel": hostel_serializer.data,
        "blocks": block_serializer.data,
        "rooms": room_serializer.data,
        "students": student_serializer.data,
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_block_data(request, pk):
    block = Block.objects.get(id=pk)
    
    rooms = Room.objects.filter(block=block)
    students = Student.objects.filter(room__in=rooms)

    block_serializer = BlockSerializer(block, many=False)
    room_serializer = RoomSerializer(rooms, many=True)
    student_serializer = StudentSerializer(students, many=True)

    data = {
        "block": block_serializer.data,
        "rooms": room_serializer.data,
        "students": student_serializer.data,
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def edit_hostel(request, pk):
    hostel = Hostel.objects.get(id=pk)
    data = json.loads(request.body)
    name = data["name"]
    secret_key = data["secretKey"]
    hostel.name = name
    hostel.secret_key = secret_key
    hostel.save()
    hostels = Hostel.objects.all()
    serializer = HostelSerializer(hostels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_hostel(request, pk):
    hostel = Hostel.objects.get(id=pk)
    hostel.delete()
    hostels = Hostel.objects.all()
    serializer = HostelSerializer(hostels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

    
    