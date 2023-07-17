from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import viewsets
from .models import Filme, Serie
from .serializers import FilmeSerializer, SerieSerializer
from metflix.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_S3_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
    URL_SQS,
)
import boto3
import uuid

"""classe responsavel pelo index, e retornar o contexto"""
sqs = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="sa-east-1",
)


class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer

    def send_message(self, message_body, message_group_id):
        sqs.send_message(
            QueueUrl=URL_SQS,
            MessageBody=message_body,
            MessageGroupId=message_group_id,
            MessageDeduplicationId=str(uuid.uuid4()),
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            filme_criado = response.data
            titulo_do_filme = filme_criado["titulo"]
            message = f"O filme {titulo_do_filme} foi criado com sucesso :)"
            self.send_message(message, titulo_do_filme)
            return redirect(reverse("index"))
        return response


class SerieViewSet(viewsets.ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer

    def send_message(self, message_body, message_group_id):
        sqs.send_message(
            QueueUrl=URL_SQS,
            MessageBody=message_body,
            MessageGroupId=message_group_id,
            MessageDeduplicationId=str(uuid.uuid4()),
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            serie_criada = response.data
            titulo_do_filme = serie_criada["titulo"]
            message = f"A série {titulo_do_filme} foi criada com sucesso :)"
            self.send_message(message, titulo_do_filme)
            return redirect(reverse("index"))
        return response
