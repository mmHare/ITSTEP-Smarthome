from django import forms

from .models import LogicController


class LogicControllerForm(forms.ModelForm):
    class Meta:
        model = LogicController
        fields = (
            'name', 'active',
            # 'logic_type',
            'numeric_min', 'numeric_max',
            'time_min', 'time_max'
        )
        widgets = {
            'time_min': forms.TimeInput(attrs={'type': 'time'}),
            'time_max': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, show_numeric=True, show_time=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not show_numeric:
            for f in ['numeric_min', 'numeric_max']:
                self.fields.pop(f, None)
        if not show_time:
            for f in ['time_min', 'time_max']:
                self.fields.pop(f, None)

    # def __init__(self, *args, show_numeric=True, show_time=True, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not show_numeric:
    #         del self.fields['numeric_max']
    #         del self.fields['numeric_min']
    #     if not show_time:
    #         del self.fields['time_max']
    #         del self.fields['time_min']
    
# class LogicControllerEditForm(forms.ModelForm):
#     class Meta:
#         model = LogicController
#         fields = (
#             'numeric_value',
#         )
