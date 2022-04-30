from tkinter.tix import AUTO
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Base for profile class
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(
        'self',
        related_name = 'followed_by',
        symmetrical=False,
        blank=True
    )

    # Makes sure on the admin page that it is not labelled as 'object 1'
    # This gives it an actual name
    def __str__(self) -> str:
        return self.user.username

# Makes it super easy to create profiles from admin page
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.friends.set([instance.profile.id])
        user_profile.save()

# The class for the posts that users can create
# Has simple attributes like when it was made and what the conent is
class UserPost(models.Model):
    user = models.ForeignKey(
        User, related_name="posts", on_delete=models.DO_NOTHING
    )

    body = models.CharField(max_length=140)
    # likes = models.ManyToManyField(User, default=None, blank=True, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Makes sure on the admin page that it is not labelled as 'object 1'
    # This gives it an actual name and useful info such as
    # Time created and created by who
    def __str__(self):
        return (
            f"{self.user}"
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )

    # Counts the number of likes
    # DOES NOT WORK CURRENTLY 
    # TBD
    @property
    def num_likes(self):
        return self.likes.all().count()

