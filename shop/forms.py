from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Fields in the form: {list(self.fields.keys())}")  # Вывод списка полей в консоль
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None
