# -*- coding: utf-8 -*-
# import json
#
# import datetime
#
# import math
# from django.conf import settings
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
# from django.shortcuts import render, render_to_response
# from django.template import RequestContext
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponseRedirect
# # from social.apps.django_app.default.models import UserSocialAuth
# from DreamsTrips.functions import is_valid_email, reset_pass
# # from experiences.models import Review, Experience, ExperienceGallery
# # from finances.models import Card, Reservation
from python_recipes import response_json, LoginRequiredMixin
from DreamsTrips import HttpResponseCodes
from profiles.models import Profile
# #
from .forms import UserRegisterForm
#     AddressUpdateForm, ProfileUpdateForm
# # from users.models import Profile, Address, ProfileGallery, Gallery, Languages
from users_functions import save_user_as_client


class UserRegisterView(TemplateView):
    """
    Creates a view from the registration form in modal.
    No it doesnt. I can't get the form fields to print with django templates
    """
    template_name = 'home.html'
    form_class = UserRegisterForm
    context = None

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context['registration_form'] = self.form_class()
        self.context = context
        return context

    def post(self, request):
        registration_form = self.form_class(request.POST or None)

        if registration_form.is_valid():
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            email = registration_form.cleaned_data['email']
            password = registration_form.cleaned_data['password1']
            user_created = save_user_as_client(first_name,
                                               last_name,
                                               email,
                                               password)
            username = email
            if user_created:
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)

                    url = reverse('home')
                    return HttpResponseRedirect(url)
        else:
            print registration_form.errors, "Errors"

            form_errors = registration_form.errors

            return response_json("%s" % form_errors,
                                 HttpResponseCodes.HTTP_409_CONFLICT)


def profile_update(request, user_pk):
    """
    Updates the user profile/info.
    :param request:
    :param user_pk: pk of the user. So far unused
    :return:
    """
    user = request.user
    profile = Profile.objects.get(auth_user=user)
    if profile.email is not None:
        profile_email = profile.email
    else:
        profile_email = None
    try:
        address = Address.objects.get(profile=profile)
    except:
        address = None

    if request.method == "POST":
        # profile_pic = request.FILES.get('picture' or None)
        first_name = request.POST.get('first_name' or None)
        last_name = request.POST.get('last_name' or None)
        email = request.POST.get('email' or None)
        languages = request.POST.getlist('languages' or None)
        if languages:
            profile_languages = profile.languages.all()
            for profile_language in profile_languages:

                profile.languages.remove(profile_language.pk)
        for language_pk in languages:
            language_obj = Languages.objects.get(pk=language_pk)
            profile.languages.add(language_obj)

        for i in range(1, 7):
            pic_file_name = 'pic_'+str(i)
            pic_file = request.FILES.get(pic_file_name)
            if pic_file is not None:
                gallery = Gallery(profile=profile, photo=pic_file)
                gallery.save()

                # DELETE PREV GALLERIES?
                profile_gallery = ProfileGallery(profile=profile,
                                                 gallery=gallery
                                                 )

                profile_gallery.save()

        # if profile_pic:
        #     profile.picture = profile_pic
        #     profile.save()

        if first_name:
            profile.auth_user.first_name = first_name
            profile.auth_user.save()

        if last_name:
            profile.auth_user.last_name = last_name
            profile.auth_user.save()

        # if email:
        #     print "EMAIL", email
        #     profile.email = email
        #     profile_email = email
        #     profile.save()

        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance=profile)
        address_form = AddressUpdateForm(data=request.POST or None,
                                         instance=address)
        card_form = CardUpdateForm(data=request.POST or None)

        address_valid = address_form.is_valid()
        profile_valid = profile_form.is_valid()
        card_valid = card_form.is_valid()

        if card_valid:
            card_form = card_form.save(commit=False)
            card_form.profile = profile
            card_form.save()

        else:
            print "Card", card_form.errors
            response = card_form.errors

        if profile_valid:
            print "Profile was valid"
            profile_form = profile_form.save(commit=False)

            if profile_form.email and profile_form.email != '' and profile_form.phone and profile_form.phone != '':
                profile_form.is_valid = True
            else:
                profile_form.is_valid = False

            profile_form.save()
        else:
            print "Profile", profile_form.errors
            response = profile_form.errors

        if address_valid:
            address_form = address_form.save(commit=False)
            address_form.profile = profile
            address_form.save()
        else:
            print "Address", address_form.errors
            response = address_form.errors

        if not profile_valid and not address_valid and not card_valid:
            return response_json("%s" % response,
                                 HttpResponseCodes.HTTP_409_CONFLICT)

        url = reverse('users:update_profile')
        return HttpResponseRedirect(url)
#
#
# def change_password(request):
#     """Changes Client password for portal
#
#     :param request:
#     :param doctype_pk:
#     :return:
#     """
#     if request.method == 'POST':
#         user = request.user
#         new_password = request.POST.get('new_password')
#         password = request.POST.get('password', None)
#         if user.check_password(password):
#             user.set_password(new_password)
#             user.save()
#
#             return HttpResponseRedirect(reverse('login_portal'))
#         else:
#             return response_json('Error', HttpResponseCodes.HTTP_401_UNAUTHORIZED)
#     else:
#         response_json('Method not allowed',
#                          HttpResponseCodes.HTTP_405_METHOD_NOT_ALLOWED)
#
#
# def user_login(request):
#     error = 'login'
#     if request.user:
#         if request.user.is_authenticated():
#             url = reverse('home')
#             return HttpResponseRedirect(url)
#     registration = request.POST.get('first_name', None)
#     if request.method == "POST" and registration is None:
#         if 'email' in request.POST and request.POST['email']:
#             if is_valid_email(request.POST['email']):
#                 # reset password
#                 reset_pass(request.POST['email'])
#                 error = "En breve recibirá un correo con su nueva contraseña."
#             else:
#                 error = 'El correo proporcionado no es v&aacute;lido'
#         else:
#             username = request.POST['username']
#             password = request.POST['password']
#
#             if '@' in username:
#                 user = authenticate(username=username, password=password)
#             else:
#                 user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     if 'rememberme' not in request.POST:
#                         request.session.set_expiry(0)
#
#                     login(request, user)
#                     url = reverse('home')
#                     try:
#                         ur_get = request.META['HTTP_REFERER']
#                     except KeyError:
#                         pass
#                     else:
#                         ur_get = ur_get.split("next=")
#                         if len(ur_get) > 1:
#                             url = ur_get[1]
#                     return HttpResponseRedirect(url)
#                 else:
#
#                     loginerror = "Tu cuenta ha sido desactivada, por favor " \
#                             "ponte en contacto con tu administrador"
#                     return response_json("%s" % loginerror,
#                                          HttpResponseCodes.HTTP_409_CONFLICT)
#             else:
#                 loginerror = "Tu nombre de usuario o contrase&ntilde;a son " \
#                         "incorrectos"
#                 return response_json("%s" % loginerror,
#                                      HttpResponseCodes.HTTP_409_CONFLICT)
#     variables = dict(error=error)
#     variables_template = RequestContext(request, variables)
#     return render_to_response("home.html", variables_template)
#
#
# def logout_page(request):
#     url = reverse('home')
#     logout(request)
#     return HttpResponseRedirect(url)
#
#
# @login_required(login_url='users:user_login')
# def update_profile_view(request):
#     address = False
#     # Admins don't have a profile. These first lines search for one and create it
#     # if it doesn't exist
#     try:
#         profile = Profile.objects.get(auth_user_id=request.user.pk)
#     except:
#         profile = Profile(auth_user=request.user)
#         profile.save()
#     try:
#         address = Address.objects.get(profile=profile)
#     except:
#         address = ''
#     if address != '':
#         address_instance = Address.objects.get(profile=profile)
#         address_form = AddressUpdateForm(instance=address_instance)
#     else:
#         address_form = AddressUpdateForm
#
#     profile_pictures = ProfileGallery.objects.filter(profile=profile)
#
#     urls = []
#     for i in range(0, 6):
#         try:
#             urls.append(profile_pictures[i].gallery.photo.url)
#         except:
#             urls.append(settings.STATIC_URL+'images/fotos-portada.png')
#
#         i += 1
#     if address != '' and address.latitude:
#         latitude = address.latitude
#     else:
#         latitude = 20.645081
#     if address != '' and address.longitude:
#         longitude = address.longitude
#     else:
#         longitude = -100.431451
#
#     context = {"request": request,
#                "user": request.user,
#                "user_form": ProfileUpdateForm(instance=profile),
#                "profile": profile,
#                "address_form": address_form,
#                "card_form": CardUpdateForm, "cards": Card.objects.filter(
#                 profile=profile
#                 ),
#                "profile_pics": urls,
#                "coordinates": json.dumps([latitude, longitude]),
#                "languages": Languages.objects.all()
#                }
#     return render(request, 'users/update_user.html', context=context)
#
#
# class ViewProfile(DetailView, LoginRequiredMixin):
#     """
#     Detail view for a user profile. Returns the single profile, as well
#     as the images related to that profile, experiences by the same
#     profile's host, the activities related to the single experience and the pertaining
#     reviews.
#     """
#     template_name = 'users/user_profile.html'
#     pk = None
#     profile = None
#     user = None
#     has_experience = False
#
#     def get_object(self, queryset=None):
#         self.user = self.request.user
#         self.pk = self.kwargs.get('profile_pk', None)
#
#         if self.pk is not None:
#             self.profile = Profile.objects.get(pk=self.pk)
#         else:
#             raise AttributeError("PK No Encontrado")
#
#         try:
#             profile_user = Profile.objects.get(auth_user=self.user)
#             experiences = Reservation.objects.filter(experience__profile=self.profile,
#                                                      profile=profile_user)
#             if len(experiences) > 0:
#                 self.has_experience = True
#         except:
#             pass
#
#         return self.profile
#
#     def get_context_data(self, **kwargs):
#         context = super(ViewProfile, self).get_context_data(**kwargs)
#         reviews = Review.objects.filter(profile=self.profile).\
#             values('profile__picture', 'review_date', 'rating', 'review', 'pk')
#
#         other_experiences = Experience.objects.filter(
#             profile=self.profile, status=Experience.ACTIVE,
#             approved=1)[:4]
#
#         for review in reviews:
#             review_obj = Review.objects.get(pk=review['pk'])
#             review['list_review'] = range(0, review['rating'])
#             review['url'] = review_obj.created_by.picture.url
#         context['profile'] = self.profile
#         context['address'] = Address.objects.filter(profile=self.profile).first()
#         context['profile_images'] = ProfileGallery.objects.filter(
#             profile=self.profile)
#         context['reviews'] = reviews
#         context['number_reviews'] = reviews.count()
#         context['review_form'] = ReviewForm
#         context['social_auth'] = UserSocialAuth.objects.filter(provider='facebook', user_id=self.profile.auth_user.pk)
#         total_reviews = [review['rating'] for review in reviews]
#         if len(total_reviews) > 0:
#             context['rating'] = range(0, int(math.floor(sum(total_reviews)/len(total_reviews))))
#         else:
#             context['rating'] = []
#         context['flag'] = 1
#         context['has_experience'] = self.has_experience
#
#         context['other_experiences'] = other_experiences
#         exp_pics = []
#         for experience in other_experiences:
#             try:
#                 pic = ExperienceGallery.objects.filter(experience=experience).first()
#                 if pic is None:
#                     exp_pics.append(experience.pk)
#                 else:
#                     exp_pics.append(pic)
#             except:
#                 print "No gallery"
#
#         context['exp_pics'] = exp_pics
#
#         return context
#
#
# @login_required(login_url='login')
# def add_review(request, pk):
#     """
#         Function to add a new review for profile or experience
#     :param request: POST
#     :param pk: Experience or Profile instance
#     :return: OK, code: 202
#     """
#     if request.method == 'POST':
#         user_profile = None
#         try:
#             user_profile = Profile.objects.get(auth_user=request.user)
#         except Profile.DoesNotExist:
#             return response_json('Invalid profile user',
#                                  HttpResponseCodes.HTTP_404_NOT_FOUND)
#         is_profile = request.POST.get('is_profile' or None)
#         review_form = ReviewForm(request.POST)
#         if review_form.is_valid():
#             review = review_form.save(commit=False)
#             if is_profile == '1':
#                 try:
#                     profile_obj = Profile.objects.get(pk=pk)
#                     review.profile = profile_obj
#                 except Profile.DoesNotExist:
#                     return response_json('Profile not found',
#                                          HttpResponseCodes.HTTP_404_NOT_FOUND)
#             else:
#                 try:
#                     experience_obj = Experience.objects.get(pk=pk)
#                     review.experience = experience_obj
#                 except Experience.DoesNotExist:
#                     return response_json('Experience not found',
#                                          HttpResponseCodes.HTTP_404_NOT_FOUND)
#             review.created_by = user_profile
#             review.review_date = datetime.date.today()
#             review.save()
#             return response_json('Ok', HttpResponseCodes.HTTP_200_OK)
#     else:
#         return response_json('Method not allowed',
#                              HttpResponseCodes.HTTP_405_METHOD_NOT_ALLOWED)
#
#
# @login_required(login_url='users:user_login')
# def save_address(request, address_pk):
#     try:
#         profile = Profile.objects.get(auth_user_id=request.user.pk)
#     except:
#         profile = Profile(auth_user=request.user)
#     if request.method == 'POST':
#
#         if address_pk != '0':
#             address_object = Address.objects.get(pk=address_pk)
#             form = AddressUpdateForm(request.POST or None, request.FILES or None,
#                                      instance=address_object)
#         else:
#             form = AddressUpdateForm(request.POST or None, request.FILES or None)
#
#         if form.is_valid():
#             address = form.save(commit=False)
#             address.profile = profile
#             address.save()
#
#             return response_json("OK", 200)
#         else:
#             return response_json("Not valid", 300)
#
#     else:
#         return response_json("Not POST", 300)
#
#
# def get_address(request, address_pk):
#     if request.method == "GET":
#         address = dict(
#             city=None,
#             address=None,
#             zipcode=None,
#             )
#         try:
#             address_obj = Address.objects.get(pk=address_pk)
#
#             address.update(
#                 city=address_obj.city.pk,
#                 address=address_obj.address,
#                 zipcode=address_obj.zipcode
#                 )
#             return response_json(address, 200)
#         except Address.DoesNotExist as e:
#             return response_json("Error", 404)
#
#     else:
#         return response_json("Method not allowed", 409)