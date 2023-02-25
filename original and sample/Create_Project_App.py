import os
import webbrowser



def create_project():
    project_name = input("Enter project name: ")
    os.system(f"django-admin startproject {project_name}")
    return project_name

def create_directory(directory_path):

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def create_app(project_name):
    app_name = input("Enter app name: ")
    os.chdir(project_name)
    os.system(f"python manage.py startapp {app_name}")
    with open(f"{project_name}/settings.py", "r") as f:
        content = f.read()
    content = content.replace(
        "    'django.contrib.staticfiles',",
        f"    'django.contrib.staticfiles',\n    '{app_name}',"
    )
    with open(f"{project_name}/settings.py", "w") as f:
        f.write(content)
    return app_name


def create_urls_file(app_name):
    with open(f"{app_name}/urls.py", "w") as f:
        f.write("from django.urls import path\nfrom . import views\n\n\n")


def create_views_file(app_name):
    with open(f"{app_name}/views.py", "w") as f:
        f.write("from django.http import HttpResponse\n\n\n")


def connect_app_urls(project_name, app_name):

# add include statement for app urls in project urls
 with open(f"{project_name}/urls.py", "r") as f:
    content = f.read()
 content = content.replace(
    """from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
""", 
     f"from django.urls import path, include\n\nurlpatterns = [\n    path('admin/', admin.site.urls),\npath('', include('{app_name}.urls')),\n]"
)
 with open(f"{project_name}/urls.py", "w") as f:
    f.write(content)

def add_url_pattern(app_name):
    with open(f"{app_name}/urls.py", "w") as f:
        f.write("from django.urls import path, include\n")
        f.write("from . import views\n\n\n")
        f.write("urlpatterns = [\n")

        while True:
            url_pattern = input("Enter URL pattern end with an / (or 'exit' to finish) code: ")

            if url_pattern == "exit":
                break
            view_function = input("Enter view function name: ")
            url_name = input("Enter URL name: ")
            response_content = input("Enter response content: ")
            f.write(f"path('{url_pattern}', views.{view_function},name='{url_name}'),\n")
            with open(f"{app_name}/views.py", "a") as f2:
                f2.write(f"def {view_function}(request):\n    return HttpResponse('{response_content}')\n\n")

        f.write("]\n")

def add_media_url(app_name):
    with open(f"{app_name}/urls.py", "a") as f:
        f.write("\nfrom django.conf import settings\n")
        f.write("from django.conf.urls.static import static\n\n")
        f.write("urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n")


def add_staticfiles_dirs(project_name):
    settings_file = os.path.join(project_name, "settings.py")
    with open(settings_file, "r") as f:
        content = f.read()
    if "STATICFILES_DIRS" not in content:
        new_line = "\nimport os \n\nSTATICFILES_DIRS = [\n    os.path.join(BASE_DIR, 'static')\n]\n"
        with open(settings_file, "a") as f:
            f.write(new_line)


def add_template_dirs(project_name):
    with open(f"{project_name}/settings.py", "r") as f:
        content = f.read()
    content = content.replace(
        
        "'DIRS': [],",
        "'DIRS': [BASE_DIR / 'templates'],"
    )
    with open(f"{project_name}/settings.py", "w") as f:
        f.write(content)


def create_templates_folder(app_name):
    path = os.path.join(app_name, 'templates')
    if not os.path.exists(path):
        os.mkdir(path)


def add_media_settings(project_name):
    with open(f"{project_name}/settings.py", "r") as f:
        content = f.read()

    media_setting = "MEDIA_URL = '/media/'\nMEDIA_ROOT = os.path.join(BASE_DIR, 'media/')"
    if media_setting not in content:
        with open(f"{project_name}/settings.py", "a") as f:
            f.write(f"\n{media_setting}\n")

def run_migrations():
    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate")


# create django project
try:
    project_name = create_project()
except:
    print('something went wrong while creating project')

# create django app inside project
try:
    app_name = create_app(project_name)
except:
    print('something went wrong while creating App')

# create urls.py file in app directory
try:
    create_urls_file(app_name)
except:
    print('something went wrong while creating Urls in app')
    
# create views.py file in app directory
try:
    create_views_file(app_name)
except:
    print('something went wrong while creating views in app')
    
# adding include statement for app urls in project urls
try:
    connect_app_urls(project_name, app_name)
except:
    print('something went wrong while including urls app in project urls')
    
# adding URL patterns and view functions name
try:
    add_url_pattern(app_name)
except:
    print('something went wrong while Adding views and urls view functions')
    
# adding templates on settings.py
try:
    add_template_dirs(project_name)
except:
    print('something went wrong while adding templates in setting asBASE_DIR')
    
# adding file in settings.py for static urls
try:
    add_staticfiles_dirs(project_name)
except:
    print('something went wrong while adding static files setting in seeting.py')
    
# adding media handling files
try:
    add_media_settings(project_name)
except:
    print('something went wrong while creating media handling files')
    
# adding media root in app urls
try:
    add_media_url(app_name)
except:
    print('something went wrong while adding media root and urls')
    
# adding templates folder in app
try:
    create_templates_folder(app_name)
except:
    print('something went wrong while creating template forlder in app')
    
# adding static folder in main project
try:
    create_directory('static')
except:
    print('something went wrong while adding static folder in BASE_DIR ')
    
# making migrations and migrate defaults table
try:
    run_migrations()
except:
    print('something went wrong while makemigrations and migrating db')
    
# creating superuser
# create = input('creating superuser with default parameters say y/n to create: ')
# print("""
#  username='admin'
#  email='admin@gmail.com'
#  password='12345'
# """)
# if 'y' in create:
#     create_super_user()
# elif 'n' in create:
#     print('Super user not created yet ')

def open_browser():
    url = "120.0.0.1:8000"
    webbrowser.open(url)




running = input('enter yes to runserver and open Browser and no to finish process: ')
if 'yes' in running:
    try:
            open_browser()
            os.system("python manage.py runserver")

    except:
            print("The running demo server has been end")
elif "no" in running:
    print(' ')
else:
    print('Your Django Project is ')