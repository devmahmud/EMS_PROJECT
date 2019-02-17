from django.shortcuts import render, get_object_or_404
from .models import Question, Answer, Choice
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'poll/home.html', context)


@login_required(login_url='user_login')
def poll_detail(request, poll_id):
    question = get_object_or_404(Question, pk=poll_id)
    context = {
        'question': question,
    }
    return render(request, 'poll/details.html', context)


@login_required(login_url='user_login')
def poll(request, poll_id=None):
    if request.method == 'GET':
        question = get_object_or_404(Question, pk=poll_id)
        return render(request, 'poll/poll.html', {'question': question})

    if request.method == 'POST':
        question = get_object_or_404(Question, pk=poll_id)
        choice = get_object_or_404(Choice, pk=request.POST.get('answer'))
        user = get_object_or_404(User, pk=request.user.id)
        Answer.objects.create(user=user, choice=choice)
        return render(request, 'poll/details.html', {'question': question})
