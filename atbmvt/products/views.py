from django.shortcuts import render
from .models import ProductImage, Product
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

def products_list(request):
    products = Product.objects.prefetch_related('images').all()
    return render(request, 'products_list.html', {'products': products})

def add_product(request):

    if request.method == "POST":
        form = ProductForm(request.POST)
        images_ids = request.POST.getlist('images')
        if form.is_valid():
            product = form.save()

            for idx, img_id in enumerate(images_ids):
                img = ProductImage.objects.get(id=img_id)
                img.product = product
                img.priority = idx
                img.save()

            return redirect("products:products_list")
    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})

def delete_product(_, product_id):
    try:
        product = Product.objects.get(id=product_id)

        for img in product.images.all():
            img.delete()

        product.delete()

    except Product.DoesNotExist:
        pass
    return redirect('products:products_list')

def edit_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('products:products_list')

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        delete_id = request.POST.get("delete_image")
        if delete_id:
            try:
                img = ProductImage.objects.get(id=delete_id, product=product)
                img.delete()
            except ProductImage.DoesNotExist:
                pass
            return redirect("products:edit_product", product_id=product.id)

        if form.is_valid():
            product.save()
            for pi in product.images.all():
                new_priority = request.POST.get(f"priority_{pi.id}")
                if new_priority is not None:
                    try:
                        pi.priority = int(new_priority)
                        pi.save()
                    except ValueError:
                        pass

            images_ids = request.POST.getlist('images')
            for idx, img_id in enumerate(images_ids):
                if not img_id:
                    continue
                try:
                    img = ProductImage.objects.get(id=img_id)
                    img.product = product
                    img.priority = idx
                    img.save()
                except (ProductImage.DoesNotExist, ValueError):
                    continue
            return redirect("products:products_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {"form": form, "product": product})

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