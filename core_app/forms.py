from django import forms
from django.contrib.auth.models import User
from django.core.files import File
import datetime
import re


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name', max_length=30, widget=forms.TextInput())
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    account_type = forms.ChoiceField(choices=[
        ('donor', 'Blood Donor'),
        ('staff', 'Medical Staff (Requires Verification)')
    ], widget=forms.RadioSelect())

    def clean(self):
        data = self.cleaned_data
        if User.objects.filter(username=data['username']).exists():
            self.add_error('username', "Username {} (already in use).".format(data['username']))
        if data.get('password1') != data.get('password2'):
            self.add_error('password2', "Unable use Password (non-matching passwords)")
        else:
            password_error = []
            if not re.search(r'.{8,}', data.get('password1')):
                password_error.append('8 characters')
            if not re.search(r'[a-z]', data.get('password1')):
                password_error.append('a lowercase')
            if not re.search(r'[A-Z]', data.get('password1')):
                password_error.append('an uppercase')
            if not re.search(r'\d', data.get('password1')):
                password_error.append('a digit')
            if not re.search(r"""(?=.*[!@#$%^&*()\\[\]{}\-_+=~`|:;'"<>,./?])""", data.get('password1')):
                password_error.append('a special character')
            if password_error:
                message = 'Password needs'
                if len(password_error) == 1:
                    message = '{}{}.'.format(message, password_error[0])
                    self.add_error('password1', message)
                else:
                    for i in range(0, len(password_error)):
                        if not i == len(password_error) - 1:
                            message = '{}, {}'.format(message, password_error[i])
                        else:
                            message = '{}, and {}.'.format(message, password_error[i])
                    self.add_error('password1', message)
        if data.get('first_name').isalpha() is False:
            self.add_error('first_name', "Invalid First Name (letters only)")
        if data.get('last_name').isalpha() is False:
            self.add_error('last_name', "Invalid Last Name (letters only)")
        if User.objects.filter(email=data['email']).exists():
            self.add_error('email', "Email {} is already in use.".format(data['email']))
        if 'staff' in data.get('account_type'):
            if User.objects.filter(username=data['username']).exists() is False:
                if re.search(r'(?<!.)MedStaff_', data['username']) is False:
                    self.add_error('account_type', "Invalid Staff Credentials (Contact HR)")
                #else:
                    #self.add_error('account_type', "Invalid Staff Credentials (Contact HR)")
            else:
                self.add_error('account_type', "Invalid Staff Credentials (Contact HR)")
        elif 'donor' in data.get('account_type'):
            if re.search(r'(?<!.)MedStaff_', data['username']):
                self.add_error('account_type', "Invalid Account Type")
        else:
            self.add_error('account_type', "Invalid Account Type")
        return data


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
        return data


class SearchForm(forms.Form):
    search_input = forms.CharField(label='Search', max_length=100, widget=forms.TextInput())

    def clean(self):
        data = self.cleaned_data
        return data


class UsernameRecoveryForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput())

    def clean(self):
        data = self.cleaned_data
        if User.objects.filter(email=data.get('email')).exists() is False:
            self.add_error('email', "Invalid Email")
        return data


class PasswordRecoveryForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput())

    def clean(self):
        data = self.cleaned_data
        if User.objects.filter(email=data.get('email')).exists() is False:
            self.add_error('email', "Invalid Email")
        return data


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
        if data.get('password1') != data.get('password2'):
            self.add_error('password2', "passwords do not match !")
        return data


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(label='Current Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='New Password', widget=forms.PasswordInput())
    password3 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
        if data.get('password2') != data.get('password3'):
            self.add_error('password3', "Unable use Password (non-matching passwords)")
        else:
            password_error = []
            if not re.search(r'.{8,}', data.get('password2')):
                password_error.append('8 characters')
            if not re.search(r'[a-z]', data.get('password2')):
                password_error.append('a lowercase')
            if not re.search(r'[A-Z]', data.get('password2')):
                password_error.append('an uppercase')
            if not re.search(r'\d', data.get('password2')):
                password_error.append('a digit')
            if not re.search(r"""(?=.*[!@#$%^&*()\\[\]{}\-_+=~`|:;'"<>,./?])""", data.get('password2')):
                password_error.append('a special character')
            if password_error:
                message = 'Password needs'
                if len(password_error) == 1:
                    message = '{}{}.'.format(message, password_error[0])
                    self.add_error('password3', message)
                else:
                    for i in range(0, len(password_error)):
                        if not i == len(password_error) - 1:
                            message = '{}, {}'.format(message, password_error[i])
                        else:
                            message = '{}, and {}.'.format(message, password_error[i])
                    self.add_error('password3', message)
        return data


"""<!--div style="border: 1px solid black; border-radius: 5px; padding: 10px; margin-bottom: 5px;">
    <form>
        <label>Profile Pic<input type="text" name="" value=""></label>
        <label>About<input type="text" name="" value=""></label>
        <label>Ratings<input type="text" name="" value=""></label>
        <label>Patient Sheets<input type="text" name="" value=""></label>
        <label>Reviews<input type="text" name="" value=""></label>
        <label>Order History<input type="text" name="" value=""></label>
        <label>Order Tracking<input type="text" name="" value=""></label>
        <label>Vacation Days(Staff)<input type="text" name="" value=""></label>
        <label>Time Sheet(Staff)<input type="text" name="" value=""></label>
    </form>
</div-->"""


class ProfileFormBloodDonor(forms.Form):
    # profile_pic = forms.ImageField()
    # profile_about = forms.CharField(label='About me:', widget=forms.TextInput())
    blood_type = forms.ChoiceField(choices=[
        ('APOS', 'A-Positive'),
        ('ANEG', 'A-Negative'),
        ('BPOS', 'B-Positive'),
        ('BNEG', 'B-Negative'),
        ('ABPOS', 'AB-Positive'),
        ('ABNEG', 'AB-Negative'),
        ('OPOS', 'O-Positive'),
        ('ONEG', 'O-Negative')
    ])
    conditions = forms.ChoiceField(choices=[
        ('0', 'None'),
        ('1', 'Aids'),
        ('2', 'Cancer'),
        ('3', 'Hepatitis'),
        ('4', 'Other'),
    ], label="Do you have any of conditions that make you ineligible?")
    # other = forms.CharField(label='Other', widget=forms.TextInput(), blank=True)

    def clean(self):
        data = self.cleaned_data
        # print(str(data) + ' from forms')
        return data


class BloodDonorAppointment(forms.Form):
    first_appointment = forms.DateField(label='First_Appointment (Desired Date) An email will be sent with available times.',
                                        initial=datetime.datetime.now() + datetime.timedelta(days=1),
                                        widget=forms.DateInput)

    def clean(self):
        data = self.cleaned_data
        # print(str(data) + ' from forms')
        return data


class BloodDonorReview(forms.Form):
    title = forms.CharField(label='Title', max_length=50, widget=forms.TextInput())
    rating = forms.IntegerField(label='Rating [1-10]', min_value=1, max_value=10)
    review = forms.CharField(label='Review', max_length=500, widget=forms.Textarea())

    def clean(self):
        data = self.cleaned_data
        print(self.errors)
        return data


class ProfileFormMedicalStaff(forms.Form):
    facility = forms.ChoiceField(choices=[
        ('BSW', 'Baylor Scott & White'),
        ('SJF', 'St. Josephs'),
        ('MMH', 'Memorial Hermann'),
    ])
    job = forms.ChoiceField(choices=[
        ('Nurse', 'Nurse'),
        ('Doctor', 'Doctor'),
        ('Admin', 'Admin')
    ])
    level = forms.IntegerField(label='Security Level', min_value=1, max_value=10)

    def clean(self):
        data = self.cleaned_data
        # print(str(data) + ' from forms')
        return data


class MedicalStaffVerify(forms.Form):
    verification = forms.CharField(label='Verification Code (Check your email)', max_length=50, widget=forms.TextInput)

    def clean(self):
        data = self.cleaned_data
        return data


class SettingsForm(forms.Form):
    setting1 = forms.CharField(label='Test2', max_length=50, widget=forms.TextInput())

    def clean(self):
        data = self.cleaned_data
        return data


class NewPatientForm(forms.Form):
    patient_id = forms.IntegerField()
    amount_donated = forms.CharField(label='Amount of Blood Donated', max_length=50, widget=forms.TextInput())
    appointment_date = forms.DateField(
        label="Appointment_Date",
        initial=datetime.datetime.now(),
        widget=forms.DateInput)
    next_eligible = forms.DateField(
        label="Next Eligible (Default 60 days)",
        initial=datetime.datetime.now() + datetime.timedelta(days=60),
        widget=forms.DateInput)
    next_appointment_date = forms.DateField(
        label="Next Appointment",
        initial=datetime.datetime.now() + datetime.timedelta(days=60),
        widget=forms.DateInput)
    special_instructions = forms.CharField(label='Special Instructions', max_length=500, widget=forms.Textarea())

    def clean(self):
        data = self.cleaned_data
        return data


class LoadPatientForms(forms.Form):
    one = forms.CharField(label='', max_length=50, widget=forms.TextInput())

    def clean(self):
        data = self.cleaned_data
        return data

class Blank(forms.Form):
    pass
