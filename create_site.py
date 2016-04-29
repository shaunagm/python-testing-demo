from mako.template import Template

mytemplate = Template("<b>hello world!</b>")

with open("index.html", "wb") as indexFile:
    indexFile.write(mytemplate.render())
