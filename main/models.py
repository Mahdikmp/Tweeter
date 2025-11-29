from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profileImages/')
    bio = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username
    

    #The func to remove the previous pic from files to reduce site's size

    def save(self, *args, **kwargs):
        #Delete previous pic
        try:
            prev = Profile.objects.get(id=self.id)
            if prev.profile_image != self.profile_image:
                if prev.profile_image and prev.profile_image.name:
                    if os.path.isfile(prev.profile_image.path):
                        os.remove(prev.profile_image.path)
        #For the time there is no profile pic
        except Profile.DoesNotExist:
            pass
    
        super().save(*args, **kwargs)

        # The func to resize the pictures before saving 
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            max_size = (250, 250)
            img.thumbnail(max_size)
            img.save(self.profile_image.path)


# Create profile for user auto
@receiver(post_save, sender = User)
def createProfile(sender, created, instance, **kwargs):
    if created:
        userProfile = Profile.objects.create(user = instance)
        userProfile.follows.add(userProfile.id)
        userProfile.save()

# post_save.connect(createProfile, sender=User)




class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tweets')
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked')

    def __str__(self):
        return (f'{self.user} in {self.created : %Y-%m-%d %H:%M} : {self.body[:30]}')
    
    def likedCount(self):
        return self.likes.count()
    
    def islikedby(self, user):
        return self.likes.filter(id=user.id).exists()
    



class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} --> {self.body[:35]}'