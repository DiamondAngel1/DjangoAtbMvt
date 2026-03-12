from django.shortcuts import redirect, render

from .models import Category
from .forms import CategoryCreateForm
from django.contrib import messages

# Create your views here.
def create_category(request):
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Категорія успішно створена.")
            return redirect('home')
    else:
        form = CategoryCreateForm()

    return render(request, 'create_category.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})