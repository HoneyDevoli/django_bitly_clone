from django.core.exceptions import ValidationError
from django.forms import ModelForm, SlugField

from ..models import Link


class LinkCreateForm(ModelForm):
    subpart = SlugField(required=False)

    class Meta:
        model = Link
        fields = ('url', 'subpart')

    def clean_subpart(self):
        subpart = self.cleaned_data.get('subpart', '')
        if subpart:
            if not Link.is_unique_subpart(subpart):
                raise ValidationError('URL abbreviation of your choice is already taken')

        return subpart
