from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    """
    Model representing a comment posted by a user. The model supports hierarchical
    comments, where replies to comments are handled via a self-referencing foreign key
    (`parent` field), allowing a comment to have replies (or be a reply itself).

    Fields:
        - user (ForeignKey): A reference to the `User` model, indicating the user who posted the comment.
        - email (EmailField): The email address associated with the comment, provided by the user.
        - home_page (URLField, optional): The URL of the user's homepage or website, if provided.
        - text (TextField): The content of the comment itself, where the user enters their message.
        - parent (ForeignKey, optional): A reference to another `Comment` object, used to define a reply.
          If `null` or `blank`, the comment is a top-level comment.
        - created_at (DateTimeField): The timestamp when the comment was created. This is set automatically
          when the comment is created.

    Meta:
        - ordering: Specifies the default ordering of comments. Comments are ordered by `created_at` in descending
          order, showing the newest comments first.
        - verbose_name: Human-readable singular name for the model.
        - verbose_name_plural: Human-readable plural name for the model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField()
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """
        Returns a string representation of the comment, showing the username of the user
        who posted the comment and the first 50 characters of the comment text.

        This representation is used when displaying the comment in Django's admin panel
        or other contexts where a string representation of the object is required.

        :return: A string combining the user's username and the first 50 characters of the text.
        """
        return f'{self.user.username}: {self.text[:50]}'
