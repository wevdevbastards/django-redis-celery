from django.shortcuts import render, redirect
from django.views import View
from .forms import DefaultForm
#from .tasks import adding_task
from redis_celery.celery import app 
from celery.result import AsyncResult

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
            task_info = app.send_task('adding_taski', (default.first_number, default.second_number))
            self.get_task_result(task_info)
            # adding_task.delay(
            #     default.first_number,
            #     default.second_number,
            # )
            return redirect('default')
    
    def get_task_result(self, task):
        work = AsyncResult(task.id)
        while True:
            if work.ready():                     # check task state: true/false
                try:
                    result = work.get(timeout=1) 
                    file = open('myfile.txt', 'w+')
                    file.write(result)
                    file.close()
                    break
                    return result
                except:
                    pass


        