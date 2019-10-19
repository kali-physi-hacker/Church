from django import forms

from .models import Member, Ministry, Shepherd


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'shepherd', 'ministry', 'telephone', 'location', 'fathers_name', 'mothers_name',
                  'guardians_name', 'new_believer_school', 'pays_tithe', 'working', 'schooling',
                  'picture']

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

        not_required = ('telephone', 'fathers_name', 'mothers_name', 'guardians_name', 'picture')
        for field in not_required:
            self.fields[field].required = False


class MinistryForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'leader', 'description']
        model = Ministry


class ShepherdForm(forms.ModelForm):
    class Meta:
        model = Shepherd
        fields = ['name', 'age']
