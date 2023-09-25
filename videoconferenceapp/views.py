from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt




# Create your views here.

def lobby(request):
    return render(request, 'lobby.html')

def room(request):
    return render(request, 'room.html')


def getToken(request):
    appId = "7e786fb79394411a9425dd4ee820e450"
    appCertificate = "c1b12bb5459340e4bcb0fcdf9ab441c9"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    
    try:
        member = RoomMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        response_data = {'message': 'Member deleted'}
    except RoomMember.DoesNotExist:
        response_data = {'message': 'Member not found'}

    return JsonResponse(response_data)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        
        # You can process and store the message as needed
        # For example, you can save it in a database
        
        # You can also broadcast the message to all users in the room
        # using WebSocket or a similar technology
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
def chatroom(request):
    return render(request, 'chatroom.html')