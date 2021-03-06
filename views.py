from django.contrib import auth
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from authtools import views as at_views
from braces import views as braces_views

from . import forms, models


# Authentication views

class LoginView(at_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('accounts:profile')

    def set_session_expiration(self, form):
        if form.cleaned_data['remember_me'] is False:
            # expires at browser close
            self.request.session.set_expiry(0)

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        self.set_session_expiration(form)
        return super().form_valid(form)


class LogoutView(at_views.LogoutView):
    url = reverse_lazy('accounts:login')


# Profile views

class ProfileViewMixin(braces_views.LoginRequiredMixin):
    """ Mixing for dealing with request.user """
    model = models.User

    def get_object(self):
        return self.request.user


class ProfileDetailView(ProfileViewMixin, generic.DetailView):
    template_name = 'accounts/profile.html'


class ProfileUpdateView(ProfileViewMixin, generic.UpdateView):
    form_class = forms.ProfileForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/profile_update.html'


class PasswordChangeView(at_views.PasswordChangeView):
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/password_change.html'


# Password reset views

class PasswordResetView(at_views.PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'accounts/password_reset_view.html'


class PasswordResetDoneView(at_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmAndLoginView(at_views.PasswordResetConfirmAndLoginView):
    template_name = 'accounts/password_reset_confirm.html'
