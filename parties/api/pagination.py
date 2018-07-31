from rest_framework import pagination


# this is the basic pagination example from rest
# it allows us to paginate our api so we only load and render
# a set amount of data each time
class StandardResultsPagination(pagination.PageNumberPagination):
	# this is the number of parties per API page
	page_size = 6
	page_size_query_param = 'page_size'
	max_page_size = 1000