import unittest
from create_site import AdorableImage, mytemplate

class AdorableImageTest(unittest.TestCase):

    def setUp(self):
        self.correctTestObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name")
        self.excessDataTestObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url",
            "www.example.com/creator_url", "A Creator's Name", "Excess data", "Even more excess data!")
        self.missingDataTestObject = AdorableImage(mytemplate, "images/image.jpg", "www.example.com/image_url")
        self.numberTestObject = AdorableImage(mytemplate, 1, 2, 3, 4)
        self.numberTestObjectWithTemplate = AdorableImage(mytemplate, 1, 2, 3, 4)

    def test_create_adorableimage_with_correct_data(self):
        self.assertIsInstance(self.correctTestObject, AdorableImage)
        self.assertEqual(self.correctTestObject.creator_name, "A Creator's Name")

    def test_adorableimage_renders_with_correct_data(self):
        self.assertEqual(self.excessDataTestObject.render(), "<img src='images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href='www.example.com/creator_url'>" +
            "A Creator's Name</a>, CC BY 0.0<br>")

    def test_create_adorableimage_with_too_much_data(self):
        self.assertIsInstance(self.excessDataTestObject, AdorableImage)

    def test_adorableimage_renders_with_too_much_data(self):
        self.assertEqual(self.excessDataTestObject.render(), "<img src='images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href='www.example.com/creator_url'>" +
            "A Creator's Name</a>, CC BY 0.0<br>")

    def test_create_adorableimage_with_too_little_data(self):
        self.assertIsInstance(self.missingDataTestObject, AdorableImage)

    def test_adorableimage_renders_with_too_little_data(self):
        self.assertEqual(self.missingDataTestObject.render(), "<img src='images/image.jpg'><p>" +
            "<a href='www.example.com/image_url'>Image</a> by <a href=''>Anonymous</a>, CC BY 0.0<br>")

    def test_create_adorableimage_with_no_data_whatsoever(self):
        with self.assertRaises(TypeError):
            testObject = AdorableImage()

    def test_create_adorableimage_with_numbers_instead_of_strings(self):
        self.assertIsInstance(self.numberTestObject, AdorableImage)

    def test_adorableimage_renders_with_numbers_instead_of_strings(self):
        self.assertEqual(self.numberTestObjectWithTemplate.render(), "<img src='1'><p><a href='2'>Image</a>" +
            " by <a href='3'>4</a>, CC BY 0.0<br>")

    def test_create_adorableimage_with_mytemplate_as_a_number(self):
        with self.assertRaises(TypeError):
            testObject = AdorableImage(99, 1, 2, 3, 4)
