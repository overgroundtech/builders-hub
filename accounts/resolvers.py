from ariadne import QueryType, MutationType, convert_kwargs_to_snake_case
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

query = QueryType()


@query.field('me')
def resolve_me(_, info):
    request = info.context["request"]
    user = request.user
    return user

resolvers = [query]