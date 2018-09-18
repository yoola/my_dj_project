from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from GoogleGlass.Image_recognition.Code.startDetection_upload import main

from GoogleGlass.models import Document
from GoogleGlass.forms import DocumentForm


def home(request):

    documents = Document.objects.all()

    if request.method == "POST":
        image_name = request.POST.get("docSelect", None)
        image_obj = request.POST.get("docSelect2", None)
        context = main("/Users/jula/Github/my_dj_project/GoogleGlass/media/"+image_name, image_obj)
        return render(request, 'GoogleGlass/image_results.html', {'context': context})

    return render(request, 'GoogleGlass/home.html', { 'documents': documents })


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'GoogleGlass/model_form_upload.html', {
        'form': form
    })

def simple_upload(request):
    if request.method == 'POST' and request.FILES['fileupload1']:
        myfile = request.FILES['fileupload1']
        print("myfile:", myfile)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'GoogleGlass/home.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'GoogleGlass/home.html')

def image_results(request):

    context = main("/Users/jula/Github/my_dj_project/GoogleGlass/media/documents/0_3_h_3OG_Flur392.jpg", "h")
    return render(request, 'GoogleGlass/image_results.html', {'context': context})

    # for j in folder:

    #     for test_path in glob.glob( os.path.join(j, '*.jpg') ):

    #         #print("test_path: ", test_path)
    #         test_img = cv2.imread(test_path)
    
    # context = test_path
    # path_ = hello()
    # context = path_ + context
    