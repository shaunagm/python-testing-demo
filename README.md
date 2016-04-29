# Learn about testing in Python!

This repository contains a demo/tutorial for learning how to test in Python.  It was created
for an [introduction to testing event](https://www.eventbrite.com/e/learn-testing-with-python-tickets-24365642292)
I ran for [PyLadies remote](http://remote.pyladies.com/).

You can follow along with the tutorial by reading through the README below.  Each section has
a corresponding branch in this repository.  You may be able to follow along with the
tutorial without checking out any additional branches but if you want to skip a section,
check your code against my code, etc., you can switch to the appropriate branch in git.  Anytime
the tutorial gets to a new section, you will be linked to the corresponding branch to check out.

In this tutorial, we will be generating a very simple website using Mako templates.  We will
first cover Python unit testing as we write the code that processes the data for the website.
Then, we'll cover integration testing (well, a form of it!) by using Selenium-Python to test that
the website appears the way we want it to.

Everything you need to know about templating in general and Mako specifically will be explained as
we go along.  Similarly, you do not need any sort of prior experience with Python unittests or with
Selenium.  You *do* need a basic knowledge of programming and Python.  If there are elements of the
tutorial that you find confusing, please feel free to open up an issue in the issue tracker and I
will respond with clarification.  I will also incorporate those explanations into the tutorial as needed.

Let's get started!

### Why testing?

^^Insert meditation on the value of testing here^^

### Setting up

If you haven't already, get this repository from Github:

    git clone https://github.com/shaunagm/python-testing-demo.git

Next, install the requirements for the demo.  I recommend using virtual environments, but it's not
strictly necessary.  If you're not using [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/),
only run the last line in this code block:

    virtualenv py-demo-env
    source py-demo-env/bin/activate
    pip install -r requirements.txt

Finally, check out the very first branch of this tutorial:

    ^^Insert branch here^^

Let's make sure that everything is working by generating our website, which should be
very simple at this point.  Type the following into your command line:

    python create_site.py

If you open up `create_site.py` you'll see that Mako is generating a template that
says "Hello world" in bold which we then save to `index.html`.  If you open up `index.html` in your
editor you see that it does indeed contain the code:

    <b>hello world!</b>

Let's make sure we can view our site in our browser.  One way to do this is to simply open up the file.  
But Python actually provides an easy way to serve up websites locally.  In your command line (you may
want to do this in a new tab so you can keep it running) type:

    python -m SimpleHTTPServer

It should tell you that it's serving HTTP on 0.0.0.0 port 8000, or something very similar.  So, you
can navigate to [http://0.0.0.0:8000/](http://0.0.0.0:8000/) in your browser.  Is it telling you and the
rest of the world hello?  Great!

That means we're ready to go.

## Section 1: Building a Simple One-Page Site

### The Code

Let's get started by creating some basic content for our website.  I am a big fan of animals,
so I want to make this website a showcase for adorable animal pictures.  Let's update our site
so that we can take an image and some data about said image and show it in `index.html`.

Open up `create_site.py`.  We want to alter our template so instead of saying "hello world!" it shows
our image.  To do this, we could simply give it the relevant image:

    mytemplate = Template("<img src='images/guinea-pig-1.jpg'>")

But that's not a method that will scale very well.  Instead, let's use Mako's variable system:

    mytemplate = Template("<img src='${image_url}'>")

    with open("index.html", "wb") as indexFile:
        indexFile.write(mytemplate.render(image_url="images/guinea-pig-1.jpg"))

Run `python create_site.py` again and refresh your browser.  You should see an adorable guinea pig!

Let's give some credit to the person who took this picture.  I found [this image](https://pixabay.com/en/guinea-pig-smooth-hair-lemonagouti-629784/) on Pixabay, a site for openly
licensed images.  Let's add that attribution to the site!  We'll add a variable to the template and populate
that variable when we render it.

    mytemplate = Template("<img src='${image_url}'><p>${image_attribution}</p>")

    with open("index.html", "wb") as indexFile:
        indexFile.write(mytemplate.render(image_url="images/guinea-pig-1.jpg",
            image_attribution="Image by Pezibear, CC BY 0.0"))

Let's add some links to that attribution, so people viewing the site can easily find the rest
of Pezibear's work.  Why don't you try changing the code so that 'Image' links to the image on Pixabay
and 'Pezibear' links to Pezibear's user page?

Great!  Let's add a second image to our website.  To do this, we just need to add a second call to
`indexFile.write(mytemplate.render())` and feed in our new data:

    indexFile.write(mytemplate.render(image_url="images/cat-1.jpg",
        pixabay_image_url="https://pixabay.com/en/kitty-cat-kitten-pet-animal-cute-551554/",
        pixabay_creator_url="https://pixabay.com/en/users/Ty_Swartz-617282/",
        creator_name="Ty_Swartz"))

(If you're copying and pasting the above, don't forget to check that my variable names and your variable names
match!)

Re-run and re-fresh, and you should see a new image with new attribution.  It looks a little funny, because we didn't
tell our template that the items should be separated by linebreaks.  Why don't you try to go ahead
and fix that?  (I chose to use a `<br>` tag to do so.  Usually it's good form to control breaks and spacing using
CSS, but we're going to avoid the complexity of adding a stylesheet.)

So now we've got two images on our site!  Excellent.  But if you look at `create_site.py`, we've
got some duplicated code.  It may be manageable now, but what if we want to show five, or fifty, or
five hundred images?  We don't want to write that out every time!

Let's make a Python object that takes a template and some data and renders it into a string:

    class AdorableImage(object):

        def __init__(self, template, image_url, pixabay_image_url, pixabay_creator_url, creator_name):
            self.template = template
            self.image_url = image_url
            self.pixabay_image_url = pixabay_image_url
            self.pixabay_creator_url = pixabay_creator_url
            self.creator_name = creator_name

        def render(self):
            return self.template.render(image_url=self.image_url, pixabay_image_url=self.pixabay_image_url,
                pixabay_creator_url=self.pixabay_creator_url, creator_name=self.creator_name)

Then, we instantiate the objects using our data and the pre-defined template:

    guineapigObject = AdorableImage(mytemplate, image_url="images/guinea-pig-1.jpg",
        pixabay_image_url="https://pixabay.com/en/guinea-pig-smooth-hair-lemonagouti-629784/",
        pixabay_creator_url="https://pixabay.com/en/users/Pezibear-526143/",
        creator_name="Pezibear")

    catObject = AdorableImage(mytemplate, image_url="images/cat-1.jpg",
        pixabay_image_url="https://pixabay.com/en/kitty-cat-kitten-pet-animal-cute-551554/",
        pixabay_creator_url="https://pixabay.com/en/users/Ty_Swartz-617282/",
        creator_name="Ty_Swartz")

Finally, we use the object's render method when writing out the file:

    with open("index.html", "wb") as indexFile:
        for item in [guineapigObject, catObject]:
            indexFile.write(item.render())

That should work!  "But Shauna!" you may be thinking.  "That's *more* code than we had before!"  True,
but most of it only needs to be written once.  The real duplication happening here is when we call AdorableImage()
multiple times to create separate objects.  Let's put the data in a separate file, comma-delimited file
and read it in in `create_site.py`:

    import csv

    adorable_image_objs = []
    with open('images.csv', 'rb') as csvfile:
        imagereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in imagereader:
            image_obj = AdorableImage(mytemplate, row[0], row[1], row[2], row[3])
            adorable_image_objs.append(image_obj)

Don't forget to actually move your data to a file names `images.csv`.  Or you can copy and paste from
[here]().

We now have a site that does what we wants and can be extended to hold as many images as we want.  I think it's
time to test it!
