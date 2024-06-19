from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ArtWorksForm
from .models import ArtWorks, Like


class DetailView(DetailView):
    template_name = 'detail.html'
    model = ArtWorks


class IndexView(ListView):
    template_name = 'index.html'
    queryset = ArtWorks.objects.order_by('-posted_at')
    paginate_by = 9

@method_decorator(login_required, name='dispatch')
class CreateWorksView(CreateView):
    form_class = ArtWorksForm
    template_name = "art_works.html"
    success_url = reverse_lazy('photo:works_done')

    def form_valid(self, form):
        worksdata = form.save(commit=False)
        worksdata.user = self.request.user
        worksdata.save()
        return super().form_valid(form)

class WorksSuccessView(TemplateView):
    template_name = 'works_success.html'

class CategoryView(ListView):
    template_name = 'index.html'
    paginate_by = 9
    
    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = ArtWorks.objects.filter(
            category=category_id).order_by('-posted_at')
        return categories

class UserView(ListView):
    template_name = 'index.html'
    paginate_by = 9
    
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = ArtWorks.objects.filter(
            user=user_id).order_by('-posted_at')
        return user_list


class ArtWorkDetailView(DetailView):
    template_name = 'detail.html'
    model = ArtWorks

class MypageView(ListView):
    template_name = 'mypage.html'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = ArtWorks.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset


class PhotoDeleteView(DeleteView):
    model = ArtWorks
    template_name ='photo_delete.html'
    success_url = reverse_lazy('photo:mypage')
    def delete(self, request, *args, **kwargs):
      return super().delete(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class LikeView(View):
    def post(self, request, *args, **kwargs):
        artwork = get_object_or_404(ArtWorks, pk=self.kwargs['pk'])
        if artwork.user == request.user:
            return JsonResponse({'error': 'You cannot like your own post'}, status=400)
        
        like, created = Like.objects.get_or_create(user=request.user, artwork=artwork)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({'liked': liked, 'count': artwork.likes.count()})
    
    
    
