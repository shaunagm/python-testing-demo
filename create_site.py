import csv
from mako.template import Template

class AdorableImage(object):

    def __init__(self, image_url="", pixabay_image_url="", pixabay_creator_url="", creator_name="Anonymous", *args):
        self.image_url = image_url
        self.pixabay_image_url = pixabay_image_url
        self.pixabay_creator_url = pixabay_creator_url
        self.creator_name = creator_name

    def render(self):
        imageTemplate = Template("<img src='../${image_url}'><p><a href='${pixabay_image_url}'>" +
            "Image</a> by <a href='${pixabay_creator_url}'>${creator_name}</a>, CC0 Public Domain<br>")
        return imageTemplate.render(image_url=self.image_url, pixabay_image_url=self.pixabay_image_url,
            pixabay_creator_url=self.pixabay_creator_url, creator_name=self.creator_name)

    def render_thumb(self):
        thumbTemplate = Template("<a href='${page_url}'><img class='thumb' src='${image_url}'></a>")
        return thumbTemplate.render(image_url=self.image_url, page_url=self.get_image_page_url())

    def get_image_page_url(self):
        return "subpages/" + self.image_url.split("/")[1].split(".")[0] + ".html"

styleTemplate = Template("<link rel='stylesheet' type='text/css' href='${path}style.css'>")

adorable_image_objs = []
with open('images.csv', 'rb') as csvfile:
    imagereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in imagereader:
        image_obj = AdorableImage(row[0], row[1], row[2], row[3])
        adorable_image_objs.append(image_obj)

with open("index.html", "wb") as indexFile:
    indexFile.write(styleTemplate.render(path=""))
    for item in adorable_image_objs:
        indexFile.write(item.render_thumb())
        with open(item.get_image_page_url(), "wb") as imageFile:
            imageFile.write(styleTemplate.render(path="../"))
            imageFile.write(item.render())
