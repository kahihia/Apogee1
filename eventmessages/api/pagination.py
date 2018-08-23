from rest_framework import pagination


# this is the basic pagination example from rest
# it allows us to paginate our api so we only load and render
# a set amount of data each time
class StandardResultsPagination(pagination.CursorPagination):
	# this is the number of parties per API page
	page_size = 30
	page_size_query_param = 'page_size'
	ordering = '-timestamp'