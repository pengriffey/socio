from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import ImageCreationForm
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import ensure_csrf_cookie
from actions.utils import create_action

# Create your views here.

@login_required
def image_list(request):
    images = Image.objects.filter(user=request.user)
    paginator = Paginator(images,10)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        #if page not an integer deliver 1st page
        images = paginator.page(1)
    except EmptyPage:
        #if request is ajax request and page is outta range deliver an empty page
        if request.is_ajax():
            return HttpResponse('')
        #deliver the last page 
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,'images/image/list_ajax.html',{'section':'images','images':images})
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():  # check if form is valid
            # cd = form.cleaned_data #get the cleaned valid data form *cleaned_data* dictionary
            new_item  = form.save(commit=False) #a new image is created but wont be saved to the db yet
            new_item.user = request.user # the current user that created the image is assigned
            new_item.save() #the new image object is saved into the database
            create_action(request.user,'shared an image', new_item)
            return redirect(new_item.get_absolute_url())
    else:
        #build the form with get request provideed by the bookmarklet 
        form = ImageCreationForm()
    return render(request,'images/image/create.html',{'section':'images',
                                                        'form':form})
                                                        
def image_detail(request,id,slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,'images/image/detail.html',{'section':'image','image':image})

@ensure_csrf_cookie    
# @ajax_required
@login_required
# @require_POST
def image_like(request):
    image_id = request.GET.get('id')
    action = request.GET.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_liked.add(request.user)
                create_action(request.user,'likes',image)
            else:
                image.users_liked.remove(request.user)
            return JsonResponse({'status':'ok','image-id':image_id,'total-likes':image.total_likes})
        except:
            pass
    return JsonResponse({'status':'ko'})

# @login_required
# def image_bookmark(request):
#     if request.method == "POST":
#         form = ImageCreationForm(data=request.POST)
#         if form.is_valid():  # check if form is valid
#             cd = form.cleaned_data  # get the cleaned valid data form *cleaned_data* dictionary
#             # a new image is created but wont be saved to the db yet
#             new_item = form.save(commit=False)
#             new_item.user = request.user  # the current user that created the image is assigned
#             new_item.save()  # the new image object is saved into the database
#             return redirect(new_item.get.absolute_ur())
#     else:
#         #build the form with get request provideed by the bookmarklet
#         form = ImageCreationForm(data=request.GET)
#     return render(request, 'images/image/create.html', {'section': 'images',
#                                                         'form': form})

