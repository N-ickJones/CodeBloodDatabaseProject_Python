# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import re
# import time
from .forms import *
from .tokens import account_activation_token
from core_settings import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib.messages import constants as messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
# from django.db import IntegrityError
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from django.views import View
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from core_app.models import ProfileImg
from django.core.files import File
from django.core.files.storage import default_storage
from core_app.Periodic.database.databaseQuery import DBQuery


# Page Settings
website_name = 'Codeblood'
page_base = 'Base-Content/base.html'
page_content = {
    'website_name': website_name,
    'submenu_top': 'SubMenu/default_top.html',
    'submenu_bottom': 'SubMenu/default_bottom.html',
    'content_top': 'Base-Content/base_content_top.html',
    'content_bottom': '',
    'login_form': LoginForm(),
    'search_form': SearchForm(),
}
# Email Settings
mail = True
website_email = website_name + '@mail.com'


def index(request):
    page_content['content_top'] = 'Base-Content/base_content_top.html'
    page_content['content_bottom'] = ''
    return render(request, page_base, page_content)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                page_content['login_alert'] = ''
                return redirect(request.POST.get('next'))
            else:
                page_content['login_alert'] = 'Invalid Credentials'
                return redirect(request.POST.get('next'))
        else:
            page_content['login_alert'] = 'Invalid Credentials'
            return redirect(request.POST.get('next'))
    else:
        return redirect('/')


def logout_view(request):
    if request.method == 'POST':
        form = request.POST
        logout(request)
        # return redirect(form.get('next'))
        return redirect('/')
    else:
        return redirect('/')


def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            return redirect('/')
        else:
            page_content['search_alert'] = 'Search Failed'
            return redirect(request.POST.get('next'))
    else:
        return redirect('/')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                            form.cleaned_data['password1'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.last_login = timezone.now()
            user.is_superuser = False
            user.is_active = False  # Cannot Login Until Email Verification
            user.is_staff = False
            user.save()
            # Start Email
            current_site = get_current_site(request)
            subject = 'Activate your ' + website_name + ' account.'
            message = render_to_string('registration/email_confirm.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            from_email = website_email
            to_list = [form.cleaned_data['email'], settings.EMAIL_HOST_USER]
            if mail:
                send_mail(subject, message, from_email, to_list, fail_silently=True)
            # End Email
            page_content['content_top'] = 'registration/email_check.html'
            page_content['content_bottom'] = ''
            return render(request, page_base, page_content)
        else:
            page_content['content_top'] = 'registration/default_form.html'
            page_content['form'] = form
            page_content['form_title'] = '{} Account Form'.format(website_name)
            return render(request, page_base, page_content)
    elif request.method == 'GET':
        form = SignupForm()
        page_content['content_top'] = 'registration/default_form.html'
        page_content['form'] = form
        page_content['form_title'] = '{} Account Form'.format(website_name)
        return render(request, page_base, page_content)
    else:
        print('Configure a ' + request.method + ' Request Method in Signup_view')


def activate(request, uidb64,  token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        page_content['content_top'] = 'registration/email_confirm_complete.html'
        page_content['content_bottom'] = ''
        return redirect('email_confirm_complete')
    else:
        page_content['content_top'] = 'registration/invalid_activation_code.html'
        return render(request, page_base, page_content)


def email_confirm_complete(request):
    page_content['content_top'] = 'registration/email_confirm_complete.html'
    page_content['content_bottom'] = ''
    return render(request, page_base, page_content)


def username_recovery(request):
    if request.method == 'POST':
        form = UsernameRecoveryForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.data['email'])
            current_site = get_current_site(request)
            subject = 'Activate your ' + website_name + ' account.'
            message = render_to_string('registration/email_username_recovery.html', {
                'user': user,
                'domain': current_site.domain,
            })
            from_email = website_email
            to_list = [form.data['email'], settings.EMAIL_HOST_USER]
            if mail:
                send_mail(subject, message, from_email, to_list, fail_silently=True)
            page_content['content_top'] = 'registration/username_sent.html'
            return render(request, page_base, page_content)
        else:
            page_content['content_top'] = 'registration/default_form.html'
            page_content['form'] = form
            page_content['form_title'] = '{} Account Form'.format(website_name)
            page_content['username_form_error'] = 'Invalid Email'
            return render(request, page_base, page_content)
    elif request.method == 'GET':
        form = UsernameRecoveryForm()
        page_content['content_top'] = 'registration/default_form.html'
        page_content['form'] = form
        page_content['form_title'] = 'Username Recovery'
        return render(request, page_base, page_content)
    else:
        print('Configure a ' + request.method + ' Request Method in Username Recovery')


def password_reset_form(request):
    if request.method == 'POST':
        form = PasswordRecoveryForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.data['email'])
            current_site = get_current_site(request)
            subject = website_name + ' Password Recovery'
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'protocol': 'http',
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            from_email = website_email
            to_list = [form.data['email'], settings.EMAIL_HOST_USER]
            if mail:
                send_mail(subject, message, from_email, to_list, fail_silently=True)
            page_content['content_top'] = 'registration/password_reset_done.html'
            return render(request, page_base, page_content)
        else:
            page_content['content_top'] = 'registration/default_form.html'
            page_content['form'] = form
            page_content['form_title'] = 'Password Recovery'
            page_content['username_form_error'] = 'Invalid Email'
            return render(request, page_base, page_content)

    elif request.method == 'GET':
        form = PasswordRecoveryForm()
        page_content['content_top'] = 'registration/default_form.html'
        page_content['form'] = form
        page_content['form_title'] = 'Password Recovery'
        return render(request, page_base, page_content)
    else:
        print('Configure a ' + request.method + ' Request Method in Password Recovery')


def password_reset_confirm(request, uidb64,  token):
    if request.method == 'POST':
        form = PasswordResetForm()
        if form.is_valid:
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None:
                user.set_password(form.cleaned_data['password2'])
                user.save()
                return redirect('/password_reset_complete')
            else:
                return redirect('/invalid_activation_code')
        else:
            page_content['content_top'] = 'registration/default_form.html'
            page_content['form'] = form
            page_content['form_title'] = 'Password Recovery'
            return render(request, page_base, page_content)
    if request.method == 'GET':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = PasswordResetForm()
            page_content['email'] = user.email
            page_content['content_top'] = 'registration/default_form.html'
            page_content['form'] = form
            page_content['form_title'] = 'Password Reset'
            return render(request, page_base, page_content)
        else:
            return redirect('/invalid_activation_code')
    else:
        print('Configure a ' + request.method + ' Request Method in Password Reset Confirm')


def password_reset_complete(request):
    page_content['content_top'] = 'registration/password_reset_complete.html'
    return render(request, page_base, page_content)


def password_change_form(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                user = authenticate(username=request.user, password=form.cleaned_data['password1'])
                if user is not None:
                    user.set_password(form.cleaned_data['password3'])
                    user.save()
                    login(request, user)
                    return redirect('/password_change_complete')
                else:
                    form.add_error('password1', "Invalid Password")
                    page_content['content_top'] = 'registration/default_form.html'
                    page_content['form'] = form
                    page_content['form_title'] = 'Password Recovery'
                    return render(request, page_base, page_content)
            else:
                page_content['content_top'] = 'registration/default_form.html'
                page_content['form'] = form
                page_content['form_title'] = 'Password Recovery'
                return render(request, page_base, page_content)
        elif request.method == 'GET':
            if request.user.is_authenticated:
                form = PasswordChangeForm()
                page_content['content_top'] = 'registration/default_form.html'
                page_content['form'] = form
                page_content['form_title'] = 'Password Change'
                return render(request, page_base, page_content)
            else:
                return redirect('/')
        else:
            print('Configure a ' + request.method + ' Request Method in Password Change Form')
    else:
        return redirect('/')


def password_change_complete(request):
    page_content['content_top'] = 'registration/password_change_complete.html'
    return render(request, page_base, page_content)


def profile_view(request):

    # Blood Donor Profile
    if request.user.is_authenticated & request.user.is_staff is False:
        if request.method == 'POST':
            if request.POST.get('blood_type'):
                form = ProfileFormBloodDonor(request.POST)
                if form.is_valid():
                    if 'None' in form.cleaned_data['conditions']:
                        eligible = True
                    else:
                        eligible = False
                    DBQuery().BloodDonor().make_donor_account(form.cleaned_data['blood_type'], eligible, False, request.user.id)
                    return redirect('/profile/')
                else:
                    pass
            elif request.POST.get('first_appointment'):
                form = BloodDonorAppointment(request.POST)
                if form.is_valid():
                    DBQuery().BloodDonor().set_appointment(request.user.id, form.cleaned_data['first_appointment'])
                    return redirect('/profile/')
                else:
                    pass
            elif request.POST.get('review'):
                form = BloodDonorReview(request.POST)
                if form.is_valid():
                    patient_id = DBQuery().BloodDonor().get_patient_id(request.user.id)
                    facility_id = DBQuery().PatientForms().get_facility_id(patient_id)
                    medical_id = DBQuery().PatientForms().get_medical_id(patient_id)
                    DBQuery().PatientReviews().create_review(datetime.datetime.now(), form.cleaned_data['title'],
                                                             form.data['rating'], form.cleaned_data['review'],
                                                             patient_id, facility_id, medical_id)

                    return redirect('/profile/')
                else:
                    pass
            else:
                form = ProfileFormBloodDonor()
                page_content['content_top'] = 'registration/profile.html'
                page_content['form'] = form
                page_content['form_title'] = '{} User Profile'.format(website_name)
                return render(request, page_base, page_content)

        elif request.method == 'GET':
            # Blood Donor Registration
            page_content['content_top'] = 'registration/profile.html'
            if DBQuery().BloodDonor().get_last_donation(request.user.id) is None:
                if DBQuery().BloodDonor().check_entry(request.user.id) is False:
                    form = ProfileFormBloodDonor()
                    page_content['progress'] = '25'
                # Next
                elif DBQuery().BloodDonor().check_appointment(request.user.id):
                    form = BloodDonorAppointment()
                    page_content['progress'] = '50'
                else:
                    # TODO Fix this to be dynamic
                    appointment_date = DBQuery().BloodDonor().get_appointment(request.user.id)
                    appointment_date += datetime.timedelta(hours=9)
                    page_content['appointment_date'] = appointment_date
                    form = None
                    page_content['content_top'] = 'registration/appointment_confirm.html'
                    page_content['progress'] = '50'
            else:
                patient_id = DBQuery().BloodDonor().get_patient_id(request.user.id)
                if DBQuery().PatientReviews().check_entry(patient_id):
                    # TODO Fix this to be dynamic
                    appointment_date = DBQuery().PatientForms().get_next_appointment_date(request.user.id)
                    appointment_date += datetime.timedelta(hours=9)
                    page_content['appointment_date'] = appointment_date
                    form = None
                    page_content['content_top'] = 'registration/appointment_confirm.html'
                    # page_content['progress'] = '100'
                else:
                    last_donation = DBQuery().BloodDonor().get_last_donation(request.user.id)
                    last_appointment_date = DBQuery().PatientForms().get_last_appointment_date(request.user.id)
                    if last_donation == last_appointment_date:
                        form = BloodDonorReview()
                        page_content['progress'] = '75'
                    else:
                        form = None

            page_content['form'] = form
            page_content['form_title'] = '{} User Profile'.format(website_name)
            return render(request, page_base, page_content)

    # Medical Staff Profile
    elif request.user.is_authenticated & request.user.is_staff:
        if request.method == 'POST':
            if request.POST.get('job'):
                form = ProfileFormMedicalStaff(request.POST)
                if form.is_valid():
                    DBQuery().MedicalStaff().add_staff_entry(timezone.now(), form.cleaned_data['facility'], form.data['level'], form.cleaned_data['job'],  request.user.id)
                    # Start Email
                    current_site = get_current_site(request)
                    subject = 'Activate your ' + website_name + ' Medical Staff account.'
                    message = render_to_string('registration/medical_staff_confirm.html', {
                        'user': request.user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)).decode(),
                        'token': account_activation_token.make_token(request.user),
                    })
                    from_email = website_email
                    to_list = [request.user.email, settings.EMAIL_HOST_USER]
                    if mail:
                        send_mail(subject, message, from_email, to_list, fail_silently=True)
                    # End Email
                    return redirect('/profile/')
                else:
                    return redirect('/profile/')
            elif request.POST.get('verification'):
                form = MedicalStaffVerify(request.POST)
                if form.is_valid():
                    page_content['page_error'] = 'Valid Activation Code'
                    redirect('/profile/')
                else:
                    page_content['page_error'] = 'Invalid Activation Code'
                    return redirect('/profile/')
            else:
                redirect('/')

        elif request.method == 'GET':
            if DBQuery().MedicalStaff().check_entry(request.user.id) is False:
                form = ProfileFormMedicalStaff()
                page_content['progress'] = '5'
            else:
                if DBQuery().MedicalStaff().is_active(request.user.id) is False:
                    form = MedicalStaffVerify()
                    page_content['progress'] = '50'
                else:
                    form = Blank()
                    page_content['progress'] = '100'
            page_content['content_top'] = 'registration/profile.html'
            page_content['form'] = form
            page_content['form_title'] = '{} Staff Profile'.format(website_name)
            return render(request, page_base, page_content)

    else:
        return redirect('/')


def activate_medical_staff(request, uidb64,  token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        DBQuery().MedicalStaff().activate_account(request.user.id)
        return redirect('/profile/')
    else:
        page_content['page_error'] = 'Invalid Activation Token'
        return redirect('/profile/')


def setting_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return render(request, page_base, page_content)
        elif request.method == 'GET':
            form = SettingsForm()
            page_content['content_top'] = 'registration/settings_form.html'
            page_content['form'] = form
            page_content['form_title'] = '{} User Settings'.format(website_name)
            return render(request, page_base, page_content)
    else:
        return redirect('/')


def patient_forms(request):
    if request.user.is_authenticated & request.user.is_staff:
        if DBQuery().MedicalStaff().is_active(request.user.id):
            # Start Patient Forms

            if request.method == 'POST':
                if request.POST.get('amount_donated'):
                    form = NewPatientForm(request.POST)
                    medical_id = DBQuery().MedicalStaff().get_medical_id(request.user.id)
                    facility_id = DBQuery().MedicalStaff().get_facility_id(medical_id)
                    if form.is_valid:
                        DBQuery().PatientForms().add_entry(request.POST.get('amount_donated'), request.POST.get('appointment_date'),
                                                      request.POST.get('next_eligible'), request.POST.get('next_appointment_date'),
                                                      request.POST.get('special_instructions'), request.POST.get('patient_id'),
                                                      facility_id, medical_id)
                        DBQuery().BloodDonor().set_last_donation(request.POST.get('patient_id'), request.POST.get('appointment_date'))
                        points = int(request.POST.get('amount_donated')) / 5
                        DBQuery().Vials().add_vial('Blood', points, request.POST.get('amount_donated'), request.POST.get('patient_id'))
                        page_content['page_error'] = 'Update Successful'
                        return redirect('/patient_forms')
                    else:
                        page_content['page_error'] = 'Could Not Update or Add Entry'
                        return redirect('/patient_forms')
                else:
                    pass
                    # redirect('/patient_forms/')

            elif request.method == 'GET':
                # TODO Generate Forms From Patient Forms & add New Form

                form = NewPatientForm()
                page_content['content_top'] = 'registration/default_form.html'
                try:
                    page_content['content_bottom'] = 'registration/appointments.html'
                    page_content['appointment'] = DBQuery().PatientForms().get_upcoming_appointments()
                except:
                    pass
                page_content['form'] = form
                page_content['form_title'] = '{} Patient Forms'.format(website_name)
                return render(request, page_base, page_content)

            # End Patient Forms
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')


def reviews(request):
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        page_content['content_top'] = 'reviews/patient_reviews.html'
        all_reviews = []
        for review in DBQuery().PatientReviews().get_all_reviews():
            all_reviews += (review[0], review[1], review[2], review[3], review[4], review[5],
                            DBQuery().PatientReviews().get_username(review[6]),
                            DBQuery().PatientReviews().get_facility(review[7]),
                            DBQuery().PatientReviews().get_medical_staff(review[8])),
            # review[6] = DBQuery().PatientReviews().get_username(review[6])
            # review[7] = DBQuery().PatientReviews().get_facility()
            # review[8] = DBQuery().PatientReviews().get_medical_staff()
            # print(all_reviews)
        page_content['reviews'] = all_reviews
        page_content['form_title'] = 'Facility Patient Reviews'
        return render(request, page_base, page_content)


def vials_view(request):
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        try:
            page_content['content_top'] = 'registration/vials.html'
            page_content['points'] = DBQuery().Vials().get_points(request.user.id)
            page_content['amount_donated'] = DBQuery().Vials().get_amount_donated(request.user.id)
            return render(request, page_base, page_content)
        except:
            return redirect('/')


def patient_forms_viewing(request):

    try:
        if request.method == 'GET':
            page_content['content_top'] = 'registration/patient_forms_viewing.html'
            page_content['last_editor'] = DBQuery().MedicalStaff().get_staff_name(
                DBQuery().PatientForms().get_last_editor(request.user.id))
            page_content['next_eligible'] = DBQuery().PatientForms().get_next_eligible(
                request.user.id) + datetime.timedelta(hours=8)
            page_content['amount_donated'] = DBQuery().PatientForms().get_amount_donated(request.user.id)
            page_content['next_appointment_date'] = DBQuery().PatientForms().get_next_appointment_date(
                request.user.id) + datetime.timedelta(hours=8)
            page_content['last_appointment_date'] = DBQuery().PatientForms().get_last_appointment_date(
                request.user.id) + datetime.timedelta(hours=9)
            page_content['special_instructions'] = DBQuery().PatientForms().get_special_instructions(request.user.id)
            return render(request, page_base, page_content)
    except:
        return redirect('/')

    """  
    # , request.FILES)
      # Profile Image TODO Enable and Fix Profile Image
               # if ProfileImg.objects.filter(username=request.user):
                   # page_content['profile_picture'] = ProfileImg.objects.get(username=request.user).image.url
                       if ProfileImg.objects.filter(username=request.user):
                           profile_image = ProfileImg.objects.get(username=request.user)
                           old_image_url = profile_image.image
                           default_storage.delete(old_image_url)
                           profile_image.image = form.cleaned_data['profile_pic']
                           profile_image.save()
                       else:
                           profile_image = ProfileImg(username=request.user, image=form.cleaned_data['profile_pic'])
                           profile_image.save()

                       if ProfileImg.objects.filter(username=request.user):
                           page_content['profile_picture'] = ProfileImg.objects.get(username=request.user).image.url
                       # End Profile Pic                

                   form = Pr
   """
