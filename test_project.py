import unittest
from create_site import AdorableImage, mytemplate

class AdorableImageTest(unittest.TestCase):

    def test_create_adorableimage_with_correct_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name")
        self.assertIsInstance(testObject, AdorableImage)
        self.assertEqual(testObject.creator_name, "A Creator's Name")

    def test_adorableimage_renders_with_correct_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name")
        self.assertEqual(testObject.render(), "<img src='images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href='www.example.com/creator_url'>" +
            "A Creator's Name</a>, CC BY 0.0<br>")

    def test_create_adorableimage_with_too_much_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name", "Excess data", "Even more excess data!")
        self.assertIsInstance(testObject, AdorableImage)

    def test_adorableimage_renders_with_too_much_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name", "Excess data", "Even more excess data!")
        self.assertEqual(testObject.render(), "<img src='images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href='www.example.com/creator_url'>" +
            "A Creator's Name</a>, CC BY 0.0<br>")

    def test_create_adorableimage_with_too_little_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url")
        self.assertIsInstance(testObject, AdorableImage)

    def test_adorableimage_renders_with_too_little_data(self):
        testObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url")
        self.assertEqual(testObject.render(), "<img src='images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href=''>Anonymous</a>, CC BY 0.0<br>")

    def test_create_adorableimage_with_no_data_whatsoever(self):
        with self.assertRaises(TypeError):
            testObject = AdorableImage()

    def test_create_adorableimage_with_numbers_instead_of_strings(self):
        testObject = AdorableImage(mytemplate, 1, 2, 3, 4)
        self.assertIsInstance(testObject, AdorableImage)

    def test_adorableimage_renders_with_numbers_instead_of_stringsa(self):
        testObject = AdorableImage(mytemplate, 1, 2, 3, 4)
        self.assertEqual(testObject.render(), "<img src='1'><p><a href='2'>Image</a> by <a href='3'>4</a>, CC BY 0.0<br>")

    def test_create_adorableimage_with_mytemplate_as_a_number(self):
        with self.assertRaises(TypeError):
            testObject = AdorableImage(99, 1, 2, 3, 4)
