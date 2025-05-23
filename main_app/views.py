from django.shortcuts import render
# Import HttpResponse to send text-based responses
from django.http import HttpResponse
    # Importing HttpResponse: Notice that we import HttpResponse from django.http. This function is used to construct an HTTP response to send back to the browser, similar to res.send() in Express.
# bring in our Cat model (from main_app/models.py)
from django.views.generic.edit import CreateView
from .models import Cat

# Create your views here.

# In Django, a view function is similar to what you may know as a "route handler" in Express. It's where you define the logic that gets executed in response to a specific HTTP request.

# For our cat-collector application, let's start by creating a basic view function that will serve as the response for the home page. We'll define this function in main_app/views.py.

# define home view function, passing request object(?)
def home(request):
    # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
    # remove above line to instead render new home.html template:
    return render(request, 'home.html')

def about(request):
    # return HttpResponse('<h1>About the CatCollector</h1>')
    return render(request, 'about.html')
        # The render() shortcut in Django is similar to Express' res.render(), except for the positional request arg. Also, the .html extension is required. For more on render(), check out more in the Django docs.

# now we're removing the hardcoded data so we can render the cats added to using the ORM:
# class Cat:
#     # initialize what a cat will be
#     def __init__(self, name, breed, description, age):
#         self.name = name 
#         self.breed = breed
#         self.description = description
#         self.age = age
    
# create a list of cat instances:
# cats = [
#     Cat('Ivy', 'torbie', 'the spoiled princess', 6),
#     Cat('Spoon', 'muted tortie', 'the aggressive snuggler', 8),
#     Cat('Garbanzo', 'orange tabby', 'the old man', 10),
# ]
    
    # 🧠 Note: Everything in a Python module is automatically exported, thus, the Cat class and the cats list will be accessible in other modules.

def cat_index(request):
    # return cat objects from cat array
    cats = Cat.objects.all()
        # remember this query from using it in the ORM?
    return render(request, 'cats/index.html', {'cats': cats})

    # Just like in Express, where data is passed to templates via an object, in Django, we use a dictionary. This dictionary is passed as the third argument to Django's render function, allowing the template to access the cat data.
    
    # We organize our templates by creating a dedicated directory for each type of entity. For the cats, we'll store their templates in templates/cats.

def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # just returning one cat:
    return render(request, 'cats/detail.html', {'cat': cat})

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'

