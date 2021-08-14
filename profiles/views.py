from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Profile
from .forms import ProfileModelForm


@login_required
def my_profile_view(request):
    '''
    自分のプロフィールの表示・編集
    '''
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None, instance=profile)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    return render(request, 'profiles/my_profile.html', context)


class ProfileListView(LoginRequiredMixin, ListView):
    '''
    自分以外のユーザーを一覧表示
    '''
    model = Profile
    template_name = 'profiles/profile_list.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles_without_me(self.request.user)
        return qs


class ProfileDetailView(LoginRequiredMixin, DetailView):
    '''
    特定のユーザーの情報
    '''
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)  # slugから特定のユーザーを取得
        return profile
