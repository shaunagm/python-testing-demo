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

### The Tests

Before we start coding, let's take a moment to think about the type of things we want to test.

Our program reads in data and then outputs it into a file.  What are some of the ways that can go wrong?  

+  The data it reads in could be formatted weirdly
+  The data it reads in could be partially missing

There may be more potential issues, but let's limit ourselves for now to testing for these.  

We're going to use Python's unittest package.  We start by creating a file which will contain our tests.
Let's call it `test_project.py`.  We'll keep it in the top level directory we're working in.  In that file, we
import the unittest module as well as the relevant code we're testing:

    import unittest
    from create_site import AdorableImage, mytemplate

Every test we make is a class.  We make them by subclassing the base class, `unittest.TestCase`.  If you don't know
what subclassing means, a basic way to think of it is like pizza.  A plain cheese pizza can be considered the pizza
base class, while pepperoni pizza or green pepper pizza are subclasses that re-use the basics of pizza (bread, tomato
sauce, cheese) and customize it further.  Your subclass can override elements of the base class, for instance a "vegan
pizza" subclass might replace non-vegan cheese with vegan cheese.  Note that the classes and subclasses are not the actual
pizzas you eat, but the items on the menu.  I'm getting hungry, so I'll stop with the analogy, but basically, when we
subclass something, we extend and customize it. If you want to know more about classes and subclasses, try [Jess Hamrick's
explanation here](http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/#subclasses).

#### Defining and running tests

We'll start by creating the shell of a test:

    class MyTest(unittest.TestCase):

        def test(self):
            pass

We're not actually testing anything here, but we want to make sure that unittest is actually working.  Let's
see if it is!

Type the following into the command line:

    python -m unittest discover

You should see an output that looks like this:

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

A note: the "discover" in `python -m unittest discover` tells unittest to find all testing files and cases.  
You can also be more specific.  The following should all work:

    python -m unittest test_project
    python -m unittest test_project.MyTest
    python -m unittest test_project.MyTest.test

They all output the same thing right now because we only have one test, but after we've built out our test
suite a bit we'll see how useful this kind of precision can be.

Let's go back and customize our test case.  While we're at it, let's script to more descriptive variable names.
Let's call our class `AdorableImageTest` and our first test `test_create_adorableimage_with_correct_data`.  (All test
cases need to start with `test_`).  Within our first test, we create an AdorableImage object.  We can use the data from
images.csv, or we can create our own data for the tests.  For readability's sake, I'm going to use fake test data with short names:

    class AdorableImageTest(unittest.TestCase):

        def test_create_adorableimage_with_correct_data(self):
            testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
                "www.example.com/creator_url", "A Creator's Name")
            pass

#### Assertions

When we run the unit tests again, we see they still pass, so adding the object didn't break anything.  But we're not
actually testing anything.  Let's replace that 'pass' with an assertion.   Assertions are a method of TestCase which
allow us to make claims about the objects we're testing.  For example, let's say we want to confirm that we've created
an AdorableImage object.  We can add the following test:

    self.assertIsInstance(testObject, AdorableImage)

`assertIsInstance` takes an object and and a class and checks whether the object is of the given class.  What else might
we want to check?  Let's see whether that object has the attribute we expect it to have.

    self.assertEqual(testObject.creator_name, "A Creator's Name")

What happens if we give the test the wrong data to compare it to?  Say, we tell it to look for "A Creators Name" (no
apostrophe)?  Here's our output:

    F
    ======================================================================
    FAIL: test_create_adorableimage_with_correct_data (test_project.AdorableImageTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_project.py", line 10, in test_create_adorableimage_with_correct_data
        self.assertEqual(testObject.creator_name, "A Creators Name")
    AssertionError: "A Creator's Name" != 'A Creators Name'

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (failures=1)

The unittest suite helpfully gives us a traceback for where the test failed.  It provides us with
very useful information via the AssertionError, which gives us the value of `testObject.creator_name`
and points out that it does not in fact equal the string we gave it.  

In addition to passing tests, represented by `.`, and failing tests, represented by `F`, there's
a third kind of test result you might see - an error.  This happens whenever your test breaks before
it gets to the assertion and throws an exception.  Let's elicit one of these errors by adding an extra
parameter to our instantiation of the AdorableImage object:

    testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
        "www.example.com/creator_url", "A Creator's Name", "")

When we run the test, we get an error, represented by `E`, as well as a traceback:

    E
    ======================================================================
    ERROR: test_create_adorableimage_with_correct_data (test_project.AdorableImageTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_project.py", line 8, in test_create_adorableimage_with_correct_data
        "www.example.com/creator_url", "A Creator's Name", "")
    TypeError: __init__() takes exactly 6 arguments (7 given)

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (errors=1)

(Note: you may ask why it says you've passed given AdorableImage 7 arguments when you've only
given it 6.  The first argument, self, is passed implicitly.  You can see it in the definition of
the \__init__ method over in `create_site.py`.)

Go ahead and change your assertion back so that it passes again.  You'll note that even though we have
two assertions, `assertIsInstance` and `assertEqual`, unittest is saying that it only ran one test.
Each test method, such as `test_create_adorableimage_with_correct_data`, counts as a single test no
matter how many assertions you put in it.

There's no hard and fast rule for how many assertions to put into a test.  Some people say every
assertion should have its own test.  I tend to include a few assertions in a test if they're very
tightly linked.  Putting multiple assertions in a given test saves on code repetition.  The downside is
that if more than one of your assertions fails, only the first of those failures will actually get tested.

I'm going to leave those two assertions in our first test, but I'll make a new test to check on a different
aspect of our object: the render method.

    def test_adorableimage_renders_with_correct_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name")
        self.assertEqual(testObject.render(), "<img src='images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href='www.example.com/creator_url'>" +
            "A Creator's Name</a>, CC BY 0.0<br>")    

When you run the tests again, you should see two passing dots: `..` and the terminal should tell you it
ran two tests.

So our object seems to work when you give it the correct data, and it breaks if you give it an extra parameter.
How can we adapt our code so it deals with an extra parameter without breaking?

#### Adapting code to pass tests

Let's start by creating a new test, one which will currently throw an exception:

    def test_create_adorableimage_with_too_much_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name", "Excess data", "Even more excess data!")
        self.assertIsInstance(testObject, AdorableImage)

How can we alter our code that adding a parameter doesn't break it?  One option is to add `*args` to our object
initialization in `create_site.py`:

    class AdorableImage(object):

        def __init__(self, template, image_url, pixabay_image_url, pixabay_creator_url, creator_name, \*args):

`\*args` captures all additional non-keyword parameters and, since we never reference it again, discards them.
Now when we run our test suite, the third test passes.  We'll create a fourth test which checks that rendering
still works with too much data.  That should pass too.

So we can handle too many parameters.  How about too few?  Time for some new tests:

    def test_create_adorableimage_with_too_little_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url")
        self.assertIsInstance(testObject, AdorableImage)

    def test_adorableimage_renders_with_too_little_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url")
        self.assertEqual(testObject.render(), "<img src='images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href=''></a>, CC BY 0.0<br>")

As expected, we get an error: `TypeError: __init__() takes at least 6 arguments (4 given)`

How can we adapt our code to handle too few arguments?  Let's create some defaults for our parameters:

    def __init__(self, template="", image_url="", pixabay_image_url="", pixabay_creator_url="", creator_name="", \*args):

Our tests pass now!  Great!  Data?  We don't need no stinkin' data!

    def test_create_adorableimage_with_no_data_whatsoever(self):
        testObject = AdorableImage()
        self.assertIsInstance(testObject, AdorableImage)

    def test_adorableimage_renders_with_no_data_whatsoever(self):
        testObject = AdorableImage()
        self.assertIsInstance(testObject, AdorableImage)
        self.assertEqual(testObject.render(), "<img src=''><p><a href=''>Image</a> by <a href=''></a>, CC BY 0.0<br>")        
Oops:

    AttributeError: 'str' object has no attribute 'render'

Maybe we got carried away.  In order for our object to render, it's pretty important that we have a template, even if
all of the data we're rendering to the template is blank.  Let's remove that default for the template parameter:

    def __init__(self, template, image_url="", pixabay_image_url="", pixabay_creator_url="", creator_name="", \*args):

Now our two most recent tests are failing.  But we *want* them to fail.  If we take away this test so that our whole
suite passes, we leave ourselves open to accidentally introducing this bug again.

`assertRaises` to the rescue!

    def test_create_adorableimage_with_no_data_whatsoever(self):
        with self.assertRaises(TypeError):
            testObject = AdorableImage()

The syntax here is slightly different.  To catch the exception, we put the code within a with statement.  We specify which
exception we expect to see.  In this case, we're expecting a TypeError.

Go ahead and delete the `test_adorableimage_renders_with_no_data_whatsoever` test, as there's no point in testing whether
a non-existent object can render.

One last thought, before we move on.  Is an empty string really the best default for the creator's name?  For one thing,
there's already a default term for an unknown person that we have in English - 'anonymous'.  For another, this field is
being used to populate the text of a link.  If we have a link but not a name, we don't want to lose the ability to access
it.  So let's make our default for `creator_name` 'anonymous'.

When we run our tests again, we see this change has induced a failure:

    AssertionError: u"<img src='images/image.jpg'><p><a href='www.example.com/image_url'>Image</a> by <a href=''>Anonymous</a>, CC BY 0.0<br>" != "<img src='images/image.jpg'><p><a href='www.example.com/image_url'>Image</a> by <a href=''></a>, CC BY 0.0<br>"

Whenever we see a failing test, we have to ask ourselves a question: should we adapt the code to pass the test, or
adapt the test to fit the code?  In this particular case, we *want* the code to do what it's doing.  It's the test
we want to bring up to date.  Go ahead and change the string we're using in `test_adorableimage_renders_with_too_little_data` so that the test passes.

Our code now deals when we give AdorableImage too much or too little data.  What about when we give it the *wrong* data?

    def test_create_adorableimage_with_numbers_instead_of_strings(self):
        testObject = AdorableImage(mytemplate, 1, 2, 3, 4)
        self.assertIsInstance(testObject, AdorableImage)

    def test_adorableimage_renders_with_numbers_instead_of_stringsa(self):
        testObject = AdorableImage(mytemplate, 1, 2, 3, 4)
        self.assertEqual(testObject.render(), "<img src='1'><p><a href='2'>Image</a> by <a href='3'>4s</a>, CC BY 0.0<br>")

It looks like Mako gracefully handles converting integers to strings.  Thanks, Mako!  What about
if we pass in a number as the mytemplate parameter?

    def test_create_adorableimage_with_mytemplate_as_a_number(self):
        testObject = AdorableImage(99, 1, 2, 3, 4)
        self.assertIsInstance(testObject, AdorableImage)

It passes!  But... we don't want it to pass.  We want our AdorableImage to reject the very idea of
a number as a template!  Let's alter our AdorableImage init method so that it only accepts a Mako template
as its mytemplate parameter:

    def __init__(self, template, image_url="", pixabay_image_url="", pixabay_creator_url="", creator_name="Anonymous", \*args):
        if not template.__class__ == Template:
            raise TypeError("First parameter (template) must be a Mako template")
        self.template = template

With this code, we check the class of the first parameter passed in to make sure that it's what we're expecting.
If it's not, we raise a TypeError.  Now, when we run our tests, we get an expected error.  Use the syntax from
`test_create_adorableimage_with_no_data_whatsoever` to adapt this test so a raised error causes the test to pass.

There are other tests we could write, but this is just a demo, so let's move on.    

#### setUp and tearDown

Before we finish with this section, let's refactor our tests a little bit.  There's a fair bit of repetition from
test to test.  For instance, we create the same AdorableImage objects multiple times.  Let's put move that process to
the `setUp` method.

`setUp` and `tearDown` are special methods which get run before and after every test, respectively.  This can be useful
for DRYing up code.  It may not seem terribly necessary for our test cases - in fact, one could argue that it isn't worth
the readability hit to even create a setUp class here - but it can be *very* useful in other situations.  For instance,
if we needed to create test databases or create multiple objects at once, `setUp` and `tearDown` would be essential.

Let's go ahead and refactor our tests, even if it's of dubious utility right now. When we've moved all object creation to setUp, it looks like this:

    def setUp(self):
        self.correctTestObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name")
        self.excessDataTestObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name", "Excess data", "Even more excess data!")
        self.missingDataTestObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url")
        self.numberTestObject = AdorableImage(mytemplate, 1, 2, 3, 4)
        self.numberTestObjectWithTemplate = AdorableImage(mytemplate, 1, 2, 3, 4)

Meanwhile, there are only assertions in our test cases.

We have no plausible use for `tearDown` right now, so will skip demo-ing that and come back to it in a later section.

#### Test coverage

Finally, let's check our test coverage.  [Coverage](https://coverage.readthedocs.io/en/coverage-4.0.3/index.html) is a
tool which profiles your code and your tests and tells you what percentage of your code is covered, in units of
[statements](https://docs.python.org/2/reference/simple_stmts.html).  Type the following:

    coverage run create_site.py

You can see the results on the command line by typing:

    coverage report create_site.py

When I do that, I see:

    Name             Stmts   Miss  Cover
    ------------------------------------
    create_site.py      23      1    96%

This gives me a general sense of how much of my code is covered by tests.  This is only useful as a ballpark, though,
as just because there is a test which relates to a given statement doesn't mean the tests adequately cover all the
ways in which that statement might be used.

You can get a more detailed report with the following:

    coverage html create_site.py

Open up `htmlcov/index.html` in your browser and click on the link to create_site.py.  There, you can see
which statements were run, missing or excluded.  

Again, this more useful as a helpful guide than as a hard-and-fast metric to follow.  Still, it's a nifty
tool.

Let's move on to section 2!

## Section 2: Extending the Site to Multiple Pages

### The Code

I've gone ahead and added a few more images to our image folder and their corresponding data to images.csv.  You can
rerun `python create_site.py` to regenerate the site.  

Cute, huh?  But the site itself is not very cute.  How can we make these images more enjoyable to browse through?

Let's make our main page a series of thumbnails, all of the same size.  To do this, we'll want to finally create that
CSS file so we don't clutter up our template with styling.  We'll create a file called `style.css` and add the following:

    .thumb {
      height: 200px;
    }

Not familiar with CSS?  Basically, this notation says to find all HTML elements with class thumb and give them a height
of 200 pixels.  Width will be automatically resized proportionally.  The `.` means to search by class, while `#`
searches by ID.  Basic HTML elements like body or p are referred to bare, for instance:

    body {
      background-color: #e6e6e6;
    }

Let's make the background silver-gray while we're at it!

We need to write a reference to this stylesheet into our document.  Let's make a new template for that, `styleTemplate`.
While we're at it, let's rename our old template something more useful like `imageTemplate`.  And we'll want a separate
template for the fullsize and thumbnail versions of our images.  Let's call the latter `thumbTemplate`.

Our new templates look like this:

    imageTemplate = Template("<img src='${image_url}'><p><a href='${pixabay_image_url}'>" +
        "Image</a> by <a href='${pixabay_creator_url}'>${creator_name}</a>, CC0 Public Domain<br>")

    styleTemplate = Template("<link rel='stylesheet' type='text/css' href='style.css'>")

    thumbTemplate = Template("<img class='thumb' src='${image_url}'>")

How shall we render them?  First, let's create a new render method on our AdorableImage object so we can choose
which template to render the data to:

    def render_thumb(self):
        return self.template.render(image_url=self.image_url)     

Now, when we write out out file, we call render_thumb instead of render - at least, for the index page.  We also
render the styleTemplate just once:

    with open("index.html", "wb") as indexFile:
        indexFile.write(styleTemplate.render())
        for item in adorable_image_objs:
            indexFile.write(item.render_thumb())

Did you get an error?  Can you tell why?

When we create our AdorableImage object, we create it with what we're now calling imageTemplate.  `render_thumb()` is
using self.template, which is imageTemplate, rather than thumbTemplate.  We can fix this by also passing in thumbTemplate.
Or, we can decide not to pass in the templates, but instead define them as part of the object.  The latter seems
more elegant to me.  

I've moved the templates into the render methods:

    def render(self):
        imageTemplate = Template("<img src='${image_url}'><p><a href='${pixabay_image_url}'>" +
            "Image</a> by <a href='${pixabay_creator_url}'>${creator_name}</a>, CC0 Public Domain<br>")
        return imageTemplate.render(image_url=self.image_url, pixabay_image_url=self.pixabay_image_url,
            pixabay_creator_url=self.pixabay_creator_url, creator_name=self.creator_name)

    def render_thumb(self):
        thumbTemplate = Template("<img class='thumb' src='${image_url}'>")
        return thumbTemplate.render(image_url=self.image_url)

We can now delete references to the templates from the \__init__ method of AdorableImage as well as from the
statement where we instantiate AdorableImage objects.  

You should now be able to regenerate the page.  Success!  We have all the thumbnail images visible on the screen,
as well as a nice gray background.  

But we still want to be able to access all of the data about each object, as well as the larger version.  So let's
create a page for each full size image.  We'll do this by adding to where we are already looping through the
images:

    with open("index.html", "wb") as indexFile:
        indexFile.write(styleTemplate.render())
        for item in adorable_image_objs:
            indexFile.write(item.render_thumb())
            with open(item.get_image_page_url(), "wb") as imageFile:
                imageFile.write(item.render())

A few things of note here.  First, we call `render_thumb()` in the main loop, which prints to the index file,
and `render()` in the subloop, which prints to individual page.  Second, we've introduced a new method,
`get_image_page_url()`:

    def get_image_page_url(self):
        return "subpages/" + self.image_url.split("/")[1].split(".")[0] + ".html"

This is declared on AdorableImage and using a bit of Python string parsing to create a reasonable filename
from the name of the original image.  We can use this method within `render_thumb()` to create a link to the individual
file from the main page:

    def render_thumb(self):
        thumbTemplate = Template("<a href='${page_url}'><img class='thumb' src='${image_url}'></a>")
        return thumbTemplate.render(image_url=self.image_url, page_url=self.get_image_page_url())

You should now be able to click on the link and be brought to a new page.  Unfortunately, this page has a few problems.
For one, the image link is now broken.  Do you know why?

Because this page is in a subdirectory, our relative path to the image is not correct.  We can fix that by adding `../`
to our imageTemplate:

    imageTemplate = Template("<img src='../${image_url}'><p><a href='${pixabay_image_url}'>" +
        "Image</a> by <a href='${pixabay_creator_url}'>${creator_name}</a>, CC0 Public Domain<br>")

We're also missing our grey background.  Let's add that to all of our individual image pages.  Because the same file
is being referenced from multiple places in the directory structure, we'll need a way to pass in the relative path to
the file. I'll let you figure out how to do that (but if you're stuck, see my solution [here]()).

We're ready to get testing!

## The Tests

Before we move on to using Selenium, let's take a moment to check in on our existing tests.  They'll probably all
pass just fine, right?

We can't even run the file:

    ImportError: cannot import name mytemplate

Because we renamed our templates, we can no longer import them into our test file.  What happens when we try to import
thumbTemplate and imageTemplate instead?


    ImportError: cannot import name thumbTemplate

We've moved thumbTemplate and imageTemplate inside of our AdorableImage object definition.  On the down side, that means
we can't import them directly.  On the up side, they come prepackaged with the AdorableImage object, so we don't have
to import them at all.  Let's delete any reference to templates in our imports, as well as in our AdorableImage object
instantiation.

When we do this, we still get six failing tests.  If you scroll threw, you can see that four of them are issues with the
rendered template.  That makes sense, because we edited the template used in `render`.  Specifically, we added a relative
path to the image url.  Go in and add this to your tests.  Once you've done this, there should be two failures left, both
saying:

    AssertionError: TypeError not raised

We no longer pass in our templates when we create our AdorableImage object, so passing in a number instead of a template
object, or nothing at all, no longer raises a TypeError.  We can delete these two tests entirely.

We could add some tests for the `render_thumb` method, and someone aiming for completeness might, but I'm about to show
you another way to test that everything's rendering successfully.  Instead, let's just add a test for
`get_image_page_url()`:

    def test_get_image_page_url_with_correct_data(self):
        self.assertEqual(self.correctTestObject.get_image_page_url(), "subpages/image.html")

We can also easily check what happens with missing data:

    def test_get_image_page_url_with_missing_data(self):
        self.assertEqual(self.missingDataTestObject.get_image_page_url(), "subpages/image.html")

That passes too, so we're good, right?  Well, no: because the definition of self.missingDataTestObject is all the way
up in `setUp` it's easy to miss that `self.image_url` is not in fact missing.  What if we change the definition of the
object to use keyword parameters, and make sure that a value for image_url is not passed in?

    self.missingDataTestObject = AdorableImage(pixabay_image_url="www.example.com/image_url", creator_name="A Creator's       Name")

This introduces an error with the rendering of `test_adorableimage_renders_with_too_little_data` which we can fix easily.
That leaves the error we were trying to induce:

    IndexError: list index out of range

Our method expects an image_url of very precise form.  `self.image_url.split("/")[1].split(".")[0]` requires that there
be a / in the string so that split returns an array of at least length two.  The second split is not quite as
troublesome, since a split that finds no character of interest returns the original string in an array of length one.

There are a number of ways to solve this dilemma.  Probably the most elegant option is to move the reference to the
images folder to the template.  We need to change the following:

+  The template generation in `render` and `render_thumb`
+  The references to the image directory from the first column in images.csv
+  How we create two of our test objects in `setUp`
+  `test_adorableimage_renders_with_numbers_instead_of_strings` and `test_adorableimage_renders_with_too_little_data` need minor edits

This leaves us with an assertion error in our test of interest:

    AssertionError: 'subpages/.html' != 'subpages/image.html'

You may think is a troublesome assertion that requires refactoring in the code rather than the tests!  That's very
sensible, but let's not be sensible.  We'll change our test string to "subpages/.html" and move on with our testing.

### Selenium

Selenium is a tool for automated web browsing.  You can use it to mimic the behavior of a person on your site.
Selenium can work with many different languages, but we'll use [selenium-python](http://selenium-python.readthedocs.io/)
today.

We can use Selenium-python within the unittest structure, even though they're not precisely unit tests.  (Some people
refer to Selenium as UI unit tests, but since UI frequently depends on the successfully integration of a variety of
complicated methods, I remain uncertain of the terminology.)  Go ahead and add the following imports to `test_project`:

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

We'll create a new test class, `WebsiteUITest`.  This is a somewhat vague title, I know.  <sub>Check the timestamps on [this commit]() :(</sub>

Here's our first test:

    def test_title_is_correct(self):
        driver = webdriver.Firefox()
        driver.get("http://0.0.0.0:8000/")
        self.assertEqual(driver.title, "Adorable images!")

What's going on?  We start by creating a driver, specifying which browser we want the driver to use.  If you don't have
Firefox, you can use one of the other drivers specified [here](http://selenium-python.readthedocs.io/api.html).  Then, we
give the driver a URL to get.  If you've stopped SimpleHTTPServer for some reason, this will not work.  Actually, it still
doesn't work, because our first assertion is about the title - which we've yet to specify.  

Let's do that.  We'll change our styleTemplate:

    styleTemplate = Template("<title>${title}</title><link rel='stylesheet' type='text/css' href='${path}style.css'>")

We now need to add a title parameter when we render styleTemplate:

    with open("index.html", "wb") as indexFile:
        indexFile.write(styleTemplate.render(path="", title="Adorable images!"))
        for item in adorable_image_objs:
            indexFile.write(item.render_thumb())
            with open(item.get_image_page_url(), "wb") as imageFile:
                imageFile.write(styleTemplate.render(path="../", title="Adorable image " + item.image_url))
                imageFile.write(item.render())

(If you haven't noticed already, this is all horrifyingly bad HTML, but it renders, so we're not worrying about it.)

Success!  Except... isn't it kind of annoying that the browser stays open?  Finally, it's a job for `tearDown`:

    def tearDown(self):
        self.driver.close()

While we're at it, let's move the opening of the site to `setUp`:

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://0.0.0.0:8000/")

What else can we test?  Let's see if there are as many thumbnails as we expect on the site:

    def test_number_of_thumbnails_on_image_page(self):
        thumb_elements = self.driver.find_elements_by_class_name("thumb")
        self.assertEqual(len(thumb_elements), 7)

This passes, but it's a bit brittle.  What if we change the number of items in images.csv?  There are a
few ways to fix this.  We could, for instance, read in `images.csv` ourselves and get the number of rows in
the file.  Another option would be to create what's called a 'test fixture' - a set of data created for the purpose
of testing.  This method is brittle in its own way, as you'll need to adjust the text fixtures whenever the structure
of your production data changes.

In our particular case, we would not only have to create test fixtures but serve them up for Selenium to test.  That's
beyond the scope of this tutorial.  So let's go with the first method:

    def test_number_of_thumbnails_on_image_page(self):
        with open('images.csv', 'rb') as csvfile:
            rows_of_data = [row for row in csv.reader(csvfile, delimiter=',')]
        thumb_elements = self.driver.find_elements_by_class_name("thumb")
        self.assertEqual(len(thumb_elements), len(rows_of_data))

What else can we test?  Why don't we test whether clicking on the images does what we want it to do?

    def test_clicking_thumbnail_opens_new_page(self):
        element_to_click = self.driver.find_elements_by_class_name("thumb")[0]
        element_to_click.click()
        self.assertEqual(self.driver.title, "Adorable image guinea-pig-1.jpg")

This passes, but once again we've made a brittle test.  What if the data changes so there's a new first row?
We don't really care which animal image is first - just that we've successfully navigated to an individual page.
We've got two options here.  First, we could change our assertion to a pair of `assertIn`:

    self.assertIn("Adorable image", self.driver.title)
    self.assertIn(".jpg", self.driver.title)

(Note that the order here is important!  assertIn looks for **a** in **b** - the reverse will fail.)

This is not ideal, because the first assertIn will also match the main page and the second assertIn will fail if
we're linking to a different kind of image.

Another option is to use `assertRegexpMatches`.  This uses a regular expression to match the title.  If you're not
familiar with regular expressions, I recommend googling a tutorial.  (I have no particular one to recommend - if you do,
let me know and I'll add it! I *do* recommend [this online regex-building tool](http://regexr.com/).)  Anyway, there's
no need to get into details now.  This'll do:

    self.assertRegexpMatches(self.driver.title, '^Adorable image[\w\d\s-]+.[\w]{1,5}')

Why don't you try adding a test which clicks on the author url and sees if it goes to Pixabay?  (See my solution here[]().)

There's a lot more we can do with Selenium-Python, but we'll stop there for now.  Before we move on, let's do a bit
more refactoring.  Why, exactly, do we need to specify the Firefox webdriver for every single test?  

#### setUpClass, setUp methods, and unit test order

If we just put our driver definition in the first test, the remaining tests won't be able to pass.  Luckily, we have
another option, `setUpClass` and `tearDownClass`:

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

What happens if we put `self.driver.get("http://0.0.0.0:8000/")` in setUpClass as well, so it only runs at the beginning
of this set of tests?  Well, we made our tests with the assumption that we were starting from the index page.  Okay,
we can change that.  What if we treat the tests as a walk through the site?  The only test that needs to change is
the last one, so it assumes we start on the individual page rather than the main page:

    def test_clicking_on_author_link_goes_to_author_page_on_pixabay(self):
        # element_to_click = self.driver.find_elements_by_class_name("thumb")[0]
        # element_to_click.click()
        element_to_click = self.driver.find_elements_by_css_selector("a")[1]
        author_name = element_to_click.text
        element_to_click.click()
        self.assertIn("Pixabay", self.driver.title)
        self.assertIn(author_name, self.driver.title)

*Aaaaaaaah!*  I got three failures and an error from that!  What happened?

Unittests are **not** ordered by what comes first in the suite.  Instead, the default is to order them using the
[`cmp`](https://docs.python.org/2/library/functions.html#cmp) function which basically does an alphanumerical sort (like alphabetical but with numbers, too).  It's considered good practice to make keep unit tests separate from each other, so that they don't depend on state from test to test.  There _are_ ways around this, including naming your tests in
alphabetical order, but for the most part, it's worth the effort to keep your tests isolated.

#### Speeding things up

Your tests should all be passing, but they may not pass quickly.  Using the browser slows things down -
my test runs are averaging around 12 seconds.  Why sit through all that when we're not looking at the Selenium
part of the test suite, or are only looking at once of the Selenium-based tests?

Remember the notation for running subsets of tests?  Let's try it again now:

    python -m unittest test_project.AdorableImageTest
    python -m unittest test_project.WebsiteUITest.test_number_of_thumbnails_on_image_page

## That's all for now!

We're all done!  I hope you enjoyed the tutorial.  In the future I plan to add brief sections on fixtures and factories,
mocks, and test driven development.  If you'd like to contribute, or want to fix an error, feel free to open an issue
in [the issue tracker]().
