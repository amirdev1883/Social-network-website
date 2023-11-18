# Social network website | Django

go to setting.py and add this

#### setting.py
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Home.apps.HomeConfig",             #add this

```
#### setting.py 
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,       ######################
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```
`"APP_DIRS": True`
this code is for that if we have had not a templates directory in base directory 
django search in that app for templates 
## Add templates to project 
![](images/1.jpg "optional-title")

## Cbv in django
```python
from django.views import View
class HomeView(View):
    def get(self, request):
        return render(request , "home/index.html")
    def post(self, request):
        return render(request, "home/index.html")
```
## widget
```python
class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
```
```python
class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}))
```
you can change attribute of this tags like this
## namespace 
you should give each url in main's url a namespace 
like this
it's better to name the namespace from app's name 
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Home.urls", namespace="Home")),
    path("account/", include("account.urls", namespace="account"))
]
```
add this to urls.py in Home app
#### Home > urls.py 
```python
app_name = "Home"
```
#### account > urls.py
```python
app_name = "account"
```
```html
<a class="nav-link active" aria-current="page" href="{% url 'Home:Home' %}">Home</a>
```
`{% url 'Home:Home' %}`

#### User registration 
```python
class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'account/register.html', {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['eamil'], cd['password'])
            messages.success("you are registered successfully ", 'success')
            return redirect("Home:Home")
```
change `form = UserRegisterForm`
to this 
```python
class RegisterView(View):
    form_class = UserRegisterForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'account/register.html', {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, "you are registered successfully ", 'success')
            return redirect("Home:Home")
```

```python
class RegisterView(View):
    form_class = UserRegisterForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'account/register.html', {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, "you are registered successfully ", 'success')
            return redirect("Home:Home")
        return render(request, 'account/register.html', {"form": form})
```
I added `return render(request, 'account/register.html', {"form": form})`
because of if data was not valied it goes to resister.html and shows
the form and errors to user
```python
class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, "you are registered successfully ", 'success')
            return redirect("Home:Home")
        return render(request, self.template_name, {"form": form})
```
add `template_name = 'account/register.html'` for cleaner code

## Form validation
So far, Django will not give us an error if a 
user registers with an already entered email

#### account > forms.py 
```python
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError("this Email is already exist")
        return email
```
but `user = User.objects.filter(email=email)` this is not good for 
our website's performance so add this 
`user = User.objects.filter(email=email).exists()`

## Override clean 
```python
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError("Password must match")
```
## QuerySets are lazy 
 the act of creating a QuerySet doesn’t involve any database activity. 
 You can stack filters together all day long,
 and Django won’t actually run the query until the QuerySet is evaluated

there is some way to evaluate a queryset that you can read that in 
django documentations

[more information](https://docs.djangoproject.com/en/4.2/topics/db/queries/#:~:text=QuerySet%20s%20are%20lazy&text=In%20general%2C%20the%20results%20of,see%20When%20QuerySets%20are%20evaluated.)

## dispathch
```python
class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("Home:Home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, "you are registered successfully ", 'success')
            return redirect("Home:Home")
        return render(request, self.template_name, {"form": form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("Home:Home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "you loged in successfully ", 'success')
                return redirect("Home:Home")
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.template_name, {"form": form})
```
I added dispathch function 
## LoginRequiredMixin
```python
from django.contrib.auth.mixins import LoginRequiredMixin

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you loged out successfully', 'success')
        return redirect('Home:Home')
```
but something is wrong because your app name is account not accounts
and it's not matching whith Django default 
when a user that he doesn't loged in enter logout url it rase a error 
but we want to redirct him to login page 

if our app's name was account it fixed by Django 

but now you should fix it by your self 

##### two way 
1. got to setting.py and add this 
```python
LOGIN_URL = "/account/login/"
```

2. change login_url in this class
```python
class UserLogoutView(LoginRequiredMixin, View):
    login_url = "/account/login/"

    def get(self, request):
        logout(request)
        messages.success(request, 'you loged out successfully', 'success')
        return redirect('Home:Home')
```

## AUTHENTICATION_BACKENDS
in many websites you see that login is by email and password 
but in django's default it's by username and password 
there is many way that you can customize your login

create authenticate.py in account app
```python
from django.contrib.auth.models import User


class EmailBackend:
	def authenticate(self, request, username=None, password=None):
		try:
			user = User.objects.get(email=username)
			if user.check_password(password):
				return user
			return None
		except User.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
```
then add this to setting.py to django identify authenticate.py
```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "account.authenticate.EmailBackend",
]
```
add this end of setting.py the first one is for django authenticate 
and the second one is for us

## Posts
#### home > models.py
```python
from django.db import models
from django.contrib.auth.models import User


class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.slug} - {self.created}'
```
don't forget to migrate this codes 
if you change somthin that is related to database you have migrate the code again
but it was related to Django it don't need to migrate

## Customize admin panel

#### Home > admin.py
```python
from django.contrib import admin
from .models import post


class PostAdmin(admin.ModelAdmin):
    list_diplay = ('user', 'slug', 'updated')
    #To display our fields
    search_fields = ('slug', 'body')
    #Search into posts in there slug and body
    list_filter = ('updated',)
    #To filter our 
    prepopulated_fields = {'slug': ('body',)}
    #
    raw_id_fields = ('user', )
    #


admin.site.register(post, PostAdmin)
```
















