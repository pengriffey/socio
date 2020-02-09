from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact
from actions.utils import create_action
from actions.models import Action
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse

# Create your views here.
@login_required
def dashboard(request):
    # display all actions by default
    actions = Action.objects.filter(verb='shared an image')
    actions = actions.select_related(
        'user', 'user__profile').prefetch_related('target')

    followings_id = request.user.following.values_list('id',flat=True)
    paginator = Paginator(actions,8)
    page = request.GET.get('page')
    if followings_id:
        actions = actions.filter(user_id__in=followings_id)
        paginator = Paginator(actions, 8)

    try:
        if  request.user.profile:
            pass
    except :
        Profile.objects.create(user=request.user)
    
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        actions = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'actions/action/detail.html', {'section': 'dashboard', 'actions': actions})
    return render(request, 'account/dashboard.html', {'section': 'dashboard','actions':actions})


def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            cd = signup_form.cleaned_data
            new_user = signup_form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user,'has created an account',)
            auth_user = auth.authenticate(request,username=cd['username'],password=cd['password'])
            if auth_user is not None:
                auth.login(request, auth_user)
                messages.success(request,'youre logged in!')
                return render(request, 'account/dashboard.html', {'section': 'dashboard'})

            messages.success(request, 'You have been registered to the site successfully')
            return render(request,'account/signup_done.html',{'user': new_user})
    else:
        signup_form = SignupForm()
        return render(request,'account/signup.html',{'form': signup_form})

@login_required
def editprofile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                    data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            prof = get_object_or_404(Profile,user=request.user)
            return render(request, 'account/profile_saved.html',{'profile':prof})

    else:
        user_form = UserEditForm()
        profile_form = ProfileEditForm()
        return render(request,'account/profile_edit.html',{'user_form':user_form,
                                                            'profile_form':profile_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',{'section':'people','users':users})

@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username,is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})

@ajax_required 
# @require_POST
@login_required
def user_follow(request):
    user_id=request.GET.get('id')
    action =request.GET.get('action')
    
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user,'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
    
