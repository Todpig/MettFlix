from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy
from .models import *
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from .viewsSet import sqs
from metflix.settings import URL_SQS


class IndexView(TemplateView):
    template_name = "index.html"
    success_url = reverse_lazy("index")

    def extract_messages_from_response(self, response):
        messages = []
        if "Messages" in response:
            messages = [message["Body"] for message in response["Messages"]]
            print("Message: ", messages)
            for message in response["Messages"]:
                receipt_handle = message["ReceiptHandle"]
                self.delete_message(receipt_handle)
        return messages

    def delete_message(self, receipt_handle):
        sqs.delete_message(QueueUrl=URL_SQS, ReceiptHandle=receipt_handle)
        print("Message deleted")

    def retrieve_sqs_messages(self):
        response = sqs.receive_message(QueueUrl=URL_SQS, MaxNumberOfMessages=10)
        messages = self.extract_messages_from_response(response)
        if messages:
            return messages

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filmes"] = Filme.objects.all()
        context["series"] = Serie.objects.all()
        context["messages"] = self.retrieve_sqs_messages()
        context["data"] = datetime.today()
        return context


"""metodo que atualiza os likes"""


def put_like(request, id):
    _obra = Obra.objects.get(id=id)

    if request.method == "POST":
        _obra.like += 1
        _obra.save()

    context = {}
    context["filmes"] = Filme.objects.order_by("?").all()
    context["series"] = Serie.objects.order_by("?").all()
    return render(request, "index.html", context)


"""metodo que atualiza os dislikes"""


def put_deslike(request, id):
    _obra = Obra.objects.get(id=id)

    if request.method == "POST":
        _obra.deslike += 1
        _obra.save()

    context = {}
    context["filmes"] = Filme.objects.order_by("?").all()
    context["series"] = Serie.objects.order_by("?").all()
    return render(request, "index.html", context)


"""metodo que atualiza os downloads"""


def put_download(request, id):
    _obra = Obra.objects.get(id=id)

    if request.method == "POST":
        _obra.download += 1
        _obra.save()

    context = {}
    context["filmes"] = Filme.objects.order_by("?").all()
    context["series"] = Serie.objects.order_by("?").all()
    return render(request, "index.html", context)


class CreateFilmeView(TemplateView):
    template_name = "createFilme.html"


class CreateSerieView(TemplateView):
    template_name = "createSerie.html"


"""class que renderiza a pagina login"""


class LoginView(TemplateView):
    template_name = "login.html"
    success_url = reverse_lazy("index")


"""class que renderiza a pagina register"""


class RegisterView(TemplateView):
    template_name = "signup.html"
    success_url = reverse_lazy("index")


"""classe que renderiza uma obra"""


class ObraView(DetailView):
    model = Obra

    template_name = "obra.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


"""metodo que faz o cadatro das contas"""


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index.html")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request, template_name="index.html", context={"register_form": form}
    )


"""metodo responsavel pelo login dos usuarios"""


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Você está logado como {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Usuário ou senha inválidos")
        else:
            messages.error(request, "Usuário ou senha inválidos")
    form = AuthenticationForm()
    return render(
        request=request, template_name="index.html", context={"login_form": form}
    )
