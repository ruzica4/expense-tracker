from django.utils.translation import gettext_lazy as _
from django.db import models
from werkzeug.security import generate_password_hash, check_password_hash


# one role->many users
# one user->one role
# one user->many expenses
# one expense->one user
# one expense->one expense type
# one expense type->many expenses


class Role(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __repr__(self):
        return '<Role: name={}>'.format(self.name)


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password_hash = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)

    @property
    def password(self):
        raise AttributeError('Password can\'t be read.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(password.hash, password)

    def __repr__(self):
        return '<User: username={}>'.format(self.username)


class ExpenseType(models.Model):
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True)

    def __repr__(self):
        return '<ExpenseType: type={}>'.format(self.type)


class Expense(models.Model):
    name = models.CharField(max_length=60)
    amount = models.FloatField()
    details = models.CharField(max_length=255, blank=True)

    class Currencies(models.TextChoices):
        AUD = 'AUD', _('Australia Dollar')
        BAM = 'BAM', _('Bosnia and Herzegovina Convertible Marka')
        CAD = 'CAD', _('Canada Dollar')
        HRK = 'HRK', _('Croatia Kuna')
        EUR = 'EUR', _('Euro Member Countries')
        HUF = 'HUF', _('Hungary Forint')
        NZD = 'NZD', _('New Zealand Dollar')
        RSD = 'RSD', _('Serbia Dinar')
        GBP = 'GBP', _('United Kingdom Pound')
        USD = 'USD', _('United States Dollar')

    currency = models.CharField(
        max_length=3,
        choices=Currencies.choices,
        default=Currencies.RSD,
    )

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_type_id = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Expense: name={}>'.format(self.name)
