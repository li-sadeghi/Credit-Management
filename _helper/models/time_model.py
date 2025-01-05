from datetime import datetime

from django.db import models
from django.db.models import Manager, QuerySet


class TimeModelQuerySet(QuerySet):
    """Custom QuerySet for TimeModel that overrides the update method.

    This QuerySet includes an overridden `update` method to automatically set
    the `modified` field to the current datetime if it's not already provided
    in the update call.
    """

    def update(self, **kwargs):
        """Overridden update method to automatically set the 'modified' field."""
        if "modified" not in kwargs:
            kwargs["modified"] = datetime.now()
        return super().update(**kwargs)


class TimeModelManager(Manager.from_queryset(TimeModelQuerySet)):
    """Custom Manager for TimeModel that uses the TimeModelQuerySet."""

    pass


class TimeModel(models.Model):
    """Abstract base model that includes automatic tracking of creation and modification times.

    This model is designed to track the `created` and `modified` fields for
    any model that inherits from it. The `created` field is set automatically
    when the object is created, and the `modified` field is updated automatically
    whenever the object is saved.
    """

    objects = TimeModelManager()

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ("-created",)
        abstract = True
