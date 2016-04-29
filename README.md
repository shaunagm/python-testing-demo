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
