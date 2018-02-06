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


def verification(request):
    u_name = request.POST.get('name')
    u_pwd = request.POST.get('password')
    b_id = request.POST.get('id')
    r_gdr = request.POST.getlist('gender')
    if u_name == 'a' and u_pwd == '123':
        request.session['session_info'] = 'info'
        temp_book = Book.books.filter(id=b_id)
        return HttpResponseRedirect(reverse('Book:results') + '?id=%s' % (b_id))
    else:
        return HttpResponseForbidden('Request Denied')


def results(request):
    try:
        info = request.session['session_info']
        print('the session info find in redis is: %s' % info)
    except:
        return HttpResponseForbidden('Request Denied')
    else:
        id = request.GET.get('id')
        return render(request, 'book/results.html')


def query_ajax(request):
    book_set = Book.books.filter(name__contains='湖')
    query_result = []
    for item in book_set:
        role_set = item.role_set.all()
        for role_item in role_set:
            query_result.append({'name': role_item.name})
    context = {
        'query_result': query_result
    }
    return JsonResponse(context)


def captcha(request):
    return render(request, 'book/captcha_page.html')


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
    request.session['captcha'] = rand_str
    font = ImageFont.truetype('C:\Windows\Fonts\FREESCPT.ttf', 30)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((45, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((85, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((125, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    buf = BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')


def recognization(request):
    if request.session.get('captcha') == request.POST.get('code'):
        return HttpResponseRedirect(reverse('Book:login'))
    return HttpResponseForbidden('request denied')


def upload_image(request):
    return render(request, 'book/upload.html')


def storage(request):
    img = request.FILES.get('img')
    img_name = img.name
    print(img_name)
    path = settings.MEDIA_ROOT + 'Book/' + img_name
    temp_img = CostomizedImage()
    temp_img.path = 'Book/' + img_name
    temp_img.save()
    with open(path, 'wb+')as f:
        for gram in img.chunks():
            f.write(gram)
    return HttpResponse('Upload successfully')


def area_display(request, page_id):
    areas = Area.objects.all()
    page_manager = Paginator(areas, 10)
    context = {'areas': page_manager.page(page_id)}
    return render(request, 'book/area_info.html', context)


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
