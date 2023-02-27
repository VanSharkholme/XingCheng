from django.shortcuts import render

import poll.models
from .models import Topic, Choices


# Create your views here.


def index(request):
    context = {}
    topics = Topic.objects.all()
    context['topics'] = topics
    return render(request, 'poll/topic_lists.html', context)


def detail(request, topic_id):
    context = {}
    try:
        topic = Topic.objects.get(pk=topic_id)
        context['topic'] = topic
        choices = topic.choices_set.all()
        context['choices'] = choices
        new_sum = 0
        if request.method == 'POST':
            # print(request.POST)
            selected_choices = request.POST.getlist('choice', [])

            for choice_id in selected_choices:
                # print(choice_id)
                changed_choice = choices.get(id=choice_id)
                changed_choice.votes += 1
                changed_choice.save()

            for choice in choices:
                # print(choice.votes)
                new_sum += choice.votes
                topic.participant_num = new_sum
                topic.save()
            # print(new_sum)
            return render(request, 'poll/detail.html', context)

            pass
        else:
            return render(request, 'poll/detail.html', context)
    except poll.models.Topic.DoesNotExist:
        return render(request, 'poll/detail.html', context)
