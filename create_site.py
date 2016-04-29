import csv
from mako.template import Template

class AdorableImage(object):

    def __init__(self, template, image_url="", pixabay_image_url="", pixabay_creator_url="", creator_name="Anonymous", *args):
        if not template.__class__ == Template:
            raise TypeError("First parameter (template) must be a Mako template")
        self.template = template
        self.image_url = image_url
        self.pixabay_image_url = pixabay_image_url
        self.pixabay_creator_url = pixabay_creator_url
        self.creator_name = creator_name

    def render(self):
        return self.template.render(image_url=self.image_url, pixabay_image_url=self.pixabay_image_url,
            pixabay_creator_url=self.pixabay_creator_url, creator_name=self.creator_name)

mytemplate = Template("<img src='${image_url}'><p><a href='${pixabay_image_url}'>" +
    "Image</a> by <a href='${pixabay_creator_url}'>${creator_name}</a>, CC BY 0.0<br>")

adorable_image_objs = []
with open('images.csv', 'rb') as csvfile:
    imagereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in imagereader:
        image_obj = AdorableImage(mytemplate, row[0], row[1], row[2], row[3])
        adorable_image_objs.append(image_obj)

with open("index.html", "wb") as indexFile:
    for item in adorable_image_objs:
        indexFile.write(item.render())
