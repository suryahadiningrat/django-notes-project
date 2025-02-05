from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from notes.serializers import NoteSerializer
from .models import Note
from django.http import Http404

class NoteList(APIView):
    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response({
            "notes": serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request):
        note = NoteSerializer(data=request.data, context={'request': request})
        if note.is_valid(raise_exception=True):
            note.save()
            return Response(note.data, status=status.HTTP_201_CREATED)
        
        return Response(note.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteDetail(APIView):
    def get(self, request, pk):
        note = self.find(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def find(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        note = self.find(pk)
        serializer = NoteSerializer(note, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.find(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)