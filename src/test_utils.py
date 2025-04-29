from utils import get_query_by_tag
filename = 'src/cql_scripts/bronze_scripts.cql'
tag = 'CREATE_BRONZE_LEVEL_TABLE'

print(get_query_by_tag(filename, tag))