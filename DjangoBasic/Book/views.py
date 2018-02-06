from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.core.paginator import Paginator
from Book.models import Book, Role, Area, CostomizedImage
from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
import random


# Create your views here.

# Basic Django view example.
def book_info(request):
    book_list = Book.books.all()

    # the query set of views contains an query instance 'query', in which function __str__() is implemented
    # which could return the raw sql query command as a string
    # for example: Book.books.all().query.__str__()
    # the manager class has an attribute raw(sql) for executing raw sql command
    print(book_list.query)

    # defination for context, which would be return to visitor as response content
    context = {
        'book_list': book_list
    }
    # the response for a specific request would be rendered with a templates in given directory
    # then be returned to browser
    return render(request, 'book/book_info.html', context)


def login(request):
    return render(request, 'book/post.html')


# Example for session modification and reversing url with query parameters.
def verification(request):
    # Parameters that passed by get or post request are acquired here.
    # They are stored as key-value pairs.
    u_name = request.POST.get('name')
    u_pwd = request.POST.get('password')
    b_id = request.POST.get('id')
    r_gdr = request.POST.getlist('gender')
    if u_name == 'a' and u_pwd == '123':
        # Modify session information.
        request.session['session_info'] = 'info'
        temp_book = Book.books.filter(id=b_id)
        # Here is the example show how query arguments for post request could be combined with reversed url.
        return HttpResponseRedirect(reverse('Book:results') + '?id=%s' % (b_id))
    else:
        return HttpResponseForbidden('Request Denied')


# Example for detecting session information from request.
def results(request):
    try:
        # Read session key from request and query with it in database.
        info = request.session['session_info']
        print('the session info find in redis is: %s' % info)
    except:
        return HttpResponseForbidden('Request Denied')
    else:
        id = request.GET.get('id')
        return render(request, 'book/results.html')


# Example for handling Ajax request.
# For Ajax requests, some json-form data should be returned in JsonResponse
def query_ajax(request):
    # Querying in database.
    book_set = Book.books.filter(name__contains='湖')
    # Generating json-form data.
    query_result = []
    for item in book_set:
        role_set = item.role_set.all()
        for role_item in role_set:
            query_result.append({'name': role_item.name})
    # Building context.
    context = {
        'query_result': query_result
    }
    return JsonResponse(context)


# Captcha page.
def captcha(request):
    return render(request, 'book/captcha_page.html')


# Example for generating captcha images and return them as iamge.
def captcha_gen(request):
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 150
    height = 40
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # Store the captcha code into session for recognization.
    request.session['captcha'] = rand_str
    font = ImageFont.truetype('C:\Windows\Fonts\FREESCPT.ttf', 30)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((45, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((85, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((125, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    # Get the instance of IO buffer stream.
    buf = BytesIO()
    # Save the data as png form.
    im.save(buf, 'png')
    # Return to browser.
    return HttpResponse(buf.getvalue(), 'image/png')


# Read captcha code from database, compared with the code input.
def recognization(request):
    if request.session.get('captcha') == request.POST.get('code'):
        return HttpResponseRedirect(reverse('Book:login'))
    return HttpResponseForbidden('request denied')


# Uploading page for iamges.
def upload_image(request):
    return render(request, 'book/upload.html')


# Store the images into media folder, while store the path information into database.
def storage(request):
    # Acquiring file dat from request.
    img = request.FILES.get('img')
    img_name = img.name
    print(img_name)
    # Combine file name and media path into path for storage in database.
    path = settings.MEDIA_ROOT + 'Book/' + img_name
    # Create instance of customized image class, store its path into database.
    temp_img = CostomizedImage()
    temp_img.path = 'Book/' + img_name
    temp_img.save()
    # Store file data into media folder.
    with open(path, 'wb+')as f:
        # The function chunks() offers a safe way for serilization of data stream.
        # Do not need to worry about memory space.
        for gram in img.chunks():
            f.write(gram)
    return HttpResponse('Upload successfully')


# Examples for using paginator, a builtin class for display content in pages
def area_display(request, page_id):
    areas = Area.objects.all()
    # Create instance of paginator.
    page_manager = Paginator(areas, 10)
    context = {'areas': page_manager.page(page_id)}
    return render(request, 'book/area_info.html', context)


# Return area select page.
def area_select(request):
    return render(request, 'book/area_select.html')


def show_province(request):
    province_list = Area.objects.filter(parent__isnull=True)
    json_data = {'province_list': [{'name': x.name, 'id': x.id} for x in province_list]}
    return JsonResponse(json_data)


def show_city(request):
    city_list = Area.objects.filter(parent=request.GET.get('province_id'))
    json_data = {'city_list': [{'name': x.name, 'id': x.id} for x in city_list]}
    return JsonResponse(json_data)


def show_area(request):
    area_list = Area.objects.filter(parent=request.GET.get('city_id'))
    json_data = {'area_list': [{'name': x.name, 'id': x.id} for x in area_list]}
    return JsonResponse(json_data)
