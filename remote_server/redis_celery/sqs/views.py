from django.shortcuts import render, redirect
from django.views import View
from .forms import DefaultForm
#from .tasks import adding_task
from redis_celery.celery import app 


class DefaultView(View):
    def get(self, request):
        default_form = DefaultForm()
        context = {
            "form": default_form,
        }
        return render(request, "sqs/default.html", context)

    def post(self, request):
        default_form = DefaultForm(request.POST)

        if default_form.is_valid():
            default = default_form.save()
            app.send_task('adding_taski', (default.first_number, default.second_number))
            # adding_task.delay(
            #     default.first_number,
            #     default.second_number,
            # )
            return redirect('default')
