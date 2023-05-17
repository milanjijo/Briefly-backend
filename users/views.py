# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, SummarySerializer, ViewSerializer
from .models import User,Summary
import jwt, datetime
from django.core.files.storage import default_storage

from .summ import SummariserCosine

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        print(request.data)
        return response 

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        print(serializer)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
class LogicView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        # if request.FILES.get('audio'):
        #     audio_file = request.FILES['audio']
        #     #  Saving POST'ed file to storage
        #     file_name = default_storage.save(audio_file.name, audio_file)
        # return Response(True)

        user = User.objects.filter(id=payload['id']).first()
        name = request.data.get('name')
        # description = request.data.get(description)
        description=""
        text = ""  
        s=""
        # s,r =  SummariserCosine().generate_summary(text)
        processedtext = Summary(user= user,name=name,description=description,text=text, summary=s)
        processedtext.save()
        return Response(processedtext.text)
    
class DashboardView(APIView):
    serializer_class = SummarySerializer

    def get(self, request):
    #     token = request.COOKIES.get('jwt')

    #     if not token:
    #         raise AuthenticationFailed('Unauthenticated!')

    #     try:
    #         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    #     except jwt.ExpiredSignatureError:
    #         raise AuthenticationFailed('Unauthenticated!')
        
    #     user = User.objects.filter(id=payload['id']).first()
        queryset = Summary.objects.filter(user_id = 1)
        serializer = ViewSerializer(data=queryset, many=True)
        if serializer.is_valid():
            print(serializer.data)  
        return Response(serializer.data)
    
class EventView(APIView):
    def get(self,request, id=None):
        summary = Summary.objects.filter(id=id).first()
        serializer= SummarySerializer(summary)
        return Response(serializer.data)
        # Response(serializer.errors)

class EditView(APIView):

    def put(self,request, id=None):
        summary = Summary.objects.filter(id=id).first()
        serializer= SummarySerializer(summary, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        Response(serializer.errors)

    def delete(self, id):
        summary = Summary.objects.get(id=id)
        summary.delete()
        Response({"status" : "success"})


