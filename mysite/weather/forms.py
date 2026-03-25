from django import forms


class WeatherSearchForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label="Your Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"}),
    )
    zipcode = forms.CharField(
        max_length=5,
        min_length=5,
        label="Zip Code",
        widget=forms.TextInput(attrs={"placeholder": "e.g. 67601"}),
    )

    def clean_zipcode(self):
        zipcode = self.cleaned_data["zipcode"]
        if not zipcode.isdigit():
            raise forms.ValidationError("Zip code must contain only digits.")
        return zipcode
