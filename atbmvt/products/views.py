from django.shortcuts import render
from .models import ProductImage
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.shortcuts import redirect
import json
import uuid

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

@csrf_exempt
def upload_temp_image(request):
    if request.method == "POST":
        file_key = list(request.FILES.keys())[0]
        image_file = request.FILES[file_key]

        img = ProductImage()
        img_image = Image.open(image_file)
        if img_image.mode in ("RGBA", "P"):
            img_image = img_image.convert("RGB")

        filename = f"{uuid.uuid4().hex}.webp"
        buffer = BytesIO()
        img_image.save(buffer, format="WEBP")
        buffer.seek(0)
        img.image.save(filename, ContentFile(buffer.read()), save=True)
        
        return JsonResponse({"file_id": img.id})
    
@csrf_exempt
def delete_temp_image(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body.decode("utf-8"))
            file_id = data.get("file_id")

            if not file_id:
                return JsonResponse({"error": "file_id is required"}, status=400)
            
            try:
                img = ProductImage.objects.get(id=file_id)
                img.delete()
                return JsonResponse({"status": "ok"})
            
            except ProductImage.DoesNotExist:
                return JsonResponse({"error": "File not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)