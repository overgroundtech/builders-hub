from ariadne import make_executable_schema, QueryType, MutationType, load_schema_from_path
from shop.resolvers import resolvers as shop_resolvers
from accounts.resolvers import resolvers as user_resolvers


type_defs = load_schema_from_path('schema/schema.graphql')

query = QueryType()
mutation = MutationType()


resolvers = [query]
resolvers += shop_resolvers
resolvers += user_resolvers
schema = make_executable_schema(type_defs, resolvers)
