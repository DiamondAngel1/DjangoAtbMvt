from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .utils import save_custom_image


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if 'email' in form.cleaned_data:
                    user.username = form.cleaned_data['email']
                if 'image' in request.FILES:
                    image = request.FILES.get('image')
                    
                    user.image_small = save_custom_image(image, size=(300, 300), folder='small')
                    user.image_medium = save_custom_image(image, size=(800, 800), folder='medium')
                    user.image_large = save_custom_image(image, size=(1200, 1200), folder='large')
                user.save()
                login(request, user)
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Помилка реєстрації: {e}')
        else:
            messages.success(request, 'Помилка реєстрації. Будь ласка, перевірте введені дані.')
            
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Невірний логін або пароль.')
    else:
        form = CustomUserLoginForm()
        
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
