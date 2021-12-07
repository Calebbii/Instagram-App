from django.test import TestCase
from django.contrib.auth.models import User
from .models import Image,Profile,Comments

# Create your tests here.
class ProfileTestClass(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("Caleb","pass")
        self.profile_test = Profile(profile_image="https://res.cloudinary.com/dtbko4o5h/image/upload/v1638823511/media/images/images_3_dtpozd.jpg",bio='Student',user=self.user)
        self.profile_test.save()

    def test_instance_true(self):
        self.profile_test.save()
        self.assertTrue(isinstance(self.profile_test,Profile))

class CommentsTestClass(TestCase):
    def setUp(self):
        self.test_user = User(username = 'Feddy')
        self.test_user.save()
        self.image = Image(image = 'new_image.png',image_name = 'Girrafe',image_caption = 'Tallest animal',user = self.test_user)
        self.comments = Comments(comment = 'Stanning',image = self.image,user = self.test_user)

class ImageTestClass(TestCase):
    def setUp(self):
        self.test_user = User(username = 'Vannce')
        self.test_user.save()
        self.image = Image(image = 'image.jpeg',image_name = 'Vannce',image_caption = 'Travelling',user = self.test_user)
        self.comments = Comments(comment = 'cool',image = self.image,user = self.test_user)


    def test_instance(self):
        self.assertTrue(isinstance(self.image,Image))

    def test_display_images(self):
        self.image.save_image()
        self.image2= Image(image = 'image.jpeg',image_name = 'caleb',image_caption = 'Vacation',user = self.test_user)
        self.image2.save_image()
        dt = Image.display_images()
        self.assertEqual(len(dt),2)

    def test_save_image(self):
        self.image.save_image()
        image = Image.objects.all()
        self.assertTrue(len(image)>0)

    def test_search(self):
        self.image.save_image()
        self.image2 = Image(image = 'image.jpeg',image_name = 'caleb',image_caption = 'Vacation',user = self.test_user)
        self.image2.save_image()
        search_term = "e"
        search1 = Image.search_images(search_term)
        search2 = Image.objects.filter(image_name__icontains = search_term)
        self.assertEqual(len(search2),len(search1))

    def test_delete_image(self):
        self.image2 = Image(image = 'image.jpeg',image_name = 'caleb',image_caption = 'Vacation',user = self.test_user)
        self.image2.save_image()
        self.image.save_image()
        self.image.delete_post()
        images = Image.objects.all()
        self.assertEqual(len(images),1)