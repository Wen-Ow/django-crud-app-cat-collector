from django.shortcuts import render, redirect
# Import HttpResponse to send text-based responses
# from django.http import HttpResponse
    # Importing HttpResponse: Notice that we import HttpResponse from django.http. This function is used to construct an HTTP response to send back to the browser, similar to res.send() in Express.
# bring in our Cat model (from main_app/models.py)
# import create class-based view
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy
from .forms import FeedingForm

# Create your views here.

# In Django, a view function is similar to what you may know as a “route handler” in Express. It’s where you define the logic that gets executed in response to a specific HTTP request.

# For our cat-collector application, let’s start by creating a basic view function that will serve as the response for the home page. We’ll define this function in main_app/views.py.

# define home view function, passing request object(?)
def home(request):
    # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
    # remove above line to instead render new home.html template:
    return render(request, 'home.html')

def about(request):
    # return HttpResponse('<h1>About the CatCollector</h1>')
    return render(request, 'about.html')
        # The render() shortcut in Django is similar to Express’ res.render(), except for the positional request arg. Also, the .html extension is required. For more on render(), check out more in the Django docs.

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

    # Just like in Express, where data is passed to templates via an object, in Django, we use a dictionary. This dictionary is passed as the third argument to Django’s render function, allowing the template to access the cat data.
    
    # We organize our templates by creating a dedicated directory for each type of entity. For the cats, we’ll store their templates in templates/cats.

def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # give us all toys that exist in the db:
    # toys = Toy.objects.all()
    # comment out above line and replace with below which only gets the toys that the cat does not have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
        # The first half of this expression Toy.objects.exclude(id__in = retrieves all Toy objects that do not have an id that is in the list of associated toy ids. The exclude() method is the opposite of filter(), which means it will get all toys except those whose ids are listed in the previous query. The id__in is a field lookup that checks if the id field of the Toy model is within the provided list.
        # The second half of this expression cat.toys.all().values_list('id') retrieves a list of ids for all the toys associated with a specific cat. This is done by first accessing all toy instances linked to the cat through the many-to-many relationship (cat.toys.all()), and then narrowing the data down to just the ids of these toys using values_list('id').
    # instantiate FeedingForm to be rendered in the template:
    feeding_form = FeedingForm()
    # just returning one cat:
    # and now include feeding_form in the context (in other words: set an instance of FeedingForm and then pass it to detail.html just like we did with cat)
    return render(request, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have,
        })

# adding a class
class CatCreate(CreateView):
    model = Cat
    # commenting out the '__all__' because we've since added a third model, and we don't want a user to be able to have access to that field
    fields = ['name', 'breed', 'description', 'age']
    # previous line of code and corresponding notes:
    # fields = '__all__'
        # The fields attribute is required and can be used to limit or change the ordering of the attributes from the Cat model are generated in the ModelForm passed to the template.
        # We’ve taken advantage of the special '__all__' value to specify that the form should contain all of the Cat Model’s attributes. Alternatively, we could have listed the fields in a list like this:
            # class CatCreate(CreateView):
                # model = Cat
                # fields = ['name', 'breed', 'description', 'age']
        # IOW: different users could have different abilities 
    # success_url = '/cats/'
        # commenting this out because apparently it's an outdate way of managing a redirect to a page other than index? we're using get_absolute_url method in the model instead. 
        # you'll see in CatDelete below, we will use this code because we need the page to redirect back to index since there's no cat entry to redirect to. 
        
class CatUpdate(UpdateView):
    model = Cat
    # pass specific fields that we want the user to be able to update (compared to '__all__')
    fields = ['breed', 'description', 'age']
    
class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'
        # redirect back to the index

# best practice to actually define all functions above the classes, but for now we're placing this down here
def add_feeding(request, cat_id):
    # create ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    # The method form.is_valid() checks if the submitted form data is valid according to the form’s specifications, such as required fields being filled and data types matching the model’s requirements.
    if form.is_valid():
        # don't save the form to the db until it has the cat_id assigned
        new_feeding = form.save(commit=False)
            # After ensuring that the form contains valid data, we save the form with the commit=False option, which returns an in-memory model object so that we can assign the cat_id before actually saving to the database.
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat-detail', cat_id=cat_id)
        # Finally we will redirect instead of render since data has been changed in the database.

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'
    
class ToyList(ListView):
    model = Toy
    
class ToyDetail(DetailView):
    model = Toy
    
class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

# order matters of the passed ids
# note you can pass just the ids instead of the whole objects
def associate_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)