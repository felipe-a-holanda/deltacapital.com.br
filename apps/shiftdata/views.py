from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ShiftDataForm


class ShiftDataFormView(FormView):
    template_name = "shiftdata/shiftdata_form.html"
    form_class = ShiftDataForm
    success_url = reverse_lazy("shiftdata:result")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        result = form.call_api()
        self.request.session["cpf"] = form.cleaned_data["cpf"]
        self.request.session["result"] = result
        return super().form_valid(form)


class ShiftDataResultView(TemplateView):
    template_name = "shiftdata/shiftdata_results.html"
