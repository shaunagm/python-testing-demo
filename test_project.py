import unittest, csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from create_site import AdorableImage

class AdorableImageTest(unittest.TestCase):

    def setUp(self):
        self.correctTestObject = AdorableImage("image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name")
        self.excessDataTestObject = AdorableImage("image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name", "Excess data", "Even more excess data!")
        self.missingDataTestObject = AdorableImage(pixabay_image_url="www.example.com/image_url", creator_name="A Creator's Name")
        self.numberTestObject = AdorableImage(1, 2, 3, 4)
        self.numberTestObjectWithTemplate = AdorableImage(1, 2, 3, 4)

    def test_create_adorableimage_with_correct_data(self):
        self.assertIsInstance(self.correctTestObject, AdorableImage)
        self.assertEqual(self.correctTestObject.creator_name, "A Creator's Name")

    def test_adorableimage_renders_with_correct_data(self):
        self.assertEqual(self.excessDataTestObject.render(), "<img src='../images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href='www.example.com/creator_url'>" +
            "A Creator's Name</a>, CC0 Public Domain<br>")

    def test_create_adorableimage_with_too_much_data(self):
        self.assertIsInstance(self.excessDataTestObject, AdorableImage)

    def test_adorableimage_renders_with_too_much_data(self):
        self.assertEqual(self.excessDataTestObject.render(), "<img src='../images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href='www.example.com/creator_url'>" +
            "A Creator's Name</a>, CC0 Public Domain<br>")

    def test_create_adorableimage_with_too_little_data(self):
        self.assertIsInstance(self.missingDataTestObject, AdorableImage)

    def test_adorableimage_renders_with_too_little_data(self):
        self.assertEqual(self.missingDataTestObject.render(), "<img src='../images/'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href=''>A Creator's Name</a>, CC0 Public Domain<br>")

    def test_create_adorableimage_with_numbers_instead_of_strings(self):
        self.assertIsInstance(self.numberTestObject, AdorableImage)

    def test_adorableimage_renders_with_numbers_instead_of_strings(self):
        self.assertEqual(self.numberTestObjectWithTemplate.render(), "<img src='../images/1'><p><a href='2'>Image</a>" +
            " by <a href='3'>4</a>, CC0 Public Domain<br>")

    def test_get_image_page_url_with_correct_data(self):
        self.assertEqual(self.correctTestObject.get_image_page_url(), "subpages/image.html")

    def test_get_image_page_url_with_missing_data(self):
        self.assertEqual(self.missingDataTestObject.get_image_page_url(), "subpages/.html")

class WebsiteUITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()


    def setUp(self):
        self.driver.get("http://0.0.0.0:8000/")

    def test_title_is_correct(self):
        self.assertEqual(self.driver.title, "Adorable images!")

    def test_number_of_thumbnails_on_image_page(self):
        with open('images.csv', 'rb') as csvfile:
            rows_of_data = [row for row in csv.reader(csvfile, delimiter=',')]
        thumb_elements = self.driver.find_elements_by_class_name("thumb")
        self.assertEqual(len(thumb_elements), len(rows_of_data))

    def test_clicking_thumbnail_opens_new_page(self):
        element_to_click = self.driver.find_elements_by_class_name("thumb")[0]
        element_to_click.click()
        self.assertRegexpMatches(self.driver.title, '^Adorable image[\w\d\s-]+.[\w]{1,5}')

    def test_clicking_on_author_link_goes_to_author_page_on_pixabay(self):
        element_to_click = self.driver.find_elements_by_class_name("thumb")[0]
        element_to_click.click()
        element_to_click = self.driver.find_elements_by_css_selector("a")[1]
        author_name = element_to_click.text
        element_to_click.click()
        self.assertIn("Pixabay", self.driver.title)
        self.assertIn(author_name, self.driver.title)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
