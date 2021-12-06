from ariadne import QueryType, MutationType
from django.contrib.auth import get_user_model
from ariadne_jwt import resolve_verify, resolve_refresh, resolve_token_auth, GenericScalar
from ariadne_jwt.decorators import token_auth, login_required
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def validate_password_strength(password, password1):
    """Validates that a password is as least 7 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 8

    if password1 != password:
        raise ValidationError(_('password do not match!'))

    if len(password) < min_length:
        raise ValidationError(_(f'Password must be at least {min_length} characters '
                                'long.').format(min_length))

    # check for digit
    if not any(char.isdigit() for char in password):
        raise ValidationError(_('Password must contain at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in password):
        raise ValidationError(_('Password must contain at least 1 letter.'))


query = QueryType()


@query.field('me')
@login_required
def resolve_me(_, info):
    user = info.context["request"].user
    return user


@query.field('users')
def resolve_users(_, info):
    users = get_user_model().objects.all()
    return users


@token_auth
def resolve_token_auth(obj, info, **kwargs):
    return {"user": info.context["request"].user}


mutation = MutationType()


@mutation.field("createUser")
def resolve_create_user(_, info, username, password, password1, email):
    validate_password_strength(password, password1)
    usernames = [x.username for x in get_user_model().objects.all()]
    if username in usernames:
        raise Exception('username already taken!')

    try:
        user = get_user_model().objects.create_user(username=username, password=password, email=email)
        user.save()
        return {
            "success": True,
            "user": user
        }
    except:
        return {
            "success": False,
            "user": None
        }


mutation.set_field('verifyToken', resolve_verify)
mutation.set_field('refreshToken', resolve_refresh)
mutation.set_field('tokenAuth', resolve_token_auth)


resolvers = [query, mutation, GenericScalar]
