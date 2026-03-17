from django.shortcuts import redirect, render

from .utils import save_custom_image
from .models import Category
from .forms import CategoryCreateForm
from django.contrib import messages

# Create your views here.
def create_category(request):
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if 'image' in request.FILES:
                    category = form.save(commit=False)
                    image = request.FILES.get('image')
                    category.image = save_custom_image(image, size=(300, 300), folder='categories')
                form.save()
                messages.success(request, "Категорія успішно створена.")
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Помилка створення категорії: {e}')
    else:
        form = CategoryCreateForm()

    return render(request, 'create_category.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})