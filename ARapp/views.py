from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get(self,request,*arg,**kwargs):
        context = super(HomePageView, self).get_context_data(*kwargs)
        return render(self.request, self.template_name, context)


class TopPageView(TemplateView):
    template_name = 'toppage.html'