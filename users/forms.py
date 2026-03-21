from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor


class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': ' '}), required=False)
    emergency_contact = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    aadhaar_front = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    aadhaar_back = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '})}

    def clean_aadhaar_front(self):
        img = self.cleaned_data.get('aadhaar_front')
        if img and img.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Aadhaar image must be under 5MB.')
        return img

    def clean_aadhaar_back(self):
        img = self.cleaned_data.get('aadhaar_back')
        if img and img.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Aadhaar image must be under 5MB.')
        return img

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'patient'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                address=self.cleaned_data.get('address', ''),
                emergency_contact=self.cleaned_data.get('emergency_contact', ''),
                aadhaar_front=self.cleaned_data.get('aadhaar_front'),
                aadhaar_back=self.cleaned_data.get('aadhaar_back'),
            )
        return user


class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    specialization = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    license_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    experience_years = forms.IntegerField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    consultation_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    aadhaar_front = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    aadhaar_back = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '})}

    def clean_aadhaar_front(self):
        img = self.cleaned_data.get('aadhaar_front')
        if img and img.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Aadhaar image must be under 5MB.')
        return img

    def clean_aadhaar_back(self):
        img = self.cleaned_data.get('aadhaar_back')
        if img and img.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Aadhaar image must be under 5MB.')
        return img

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                license_number=self.cleaned_data['license_number'],
                experience_years=self.cleaned_data['experience_years'],
                consultation_fee=self.cleaned_data['consultation_fee'],
                aadhaar_front=self.cleaned_data.get('aadhaar_front'),
                aadhaar_back=self.cleaned_data.get('aadhaar_back'),
            )
        return user
