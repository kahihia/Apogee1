from django.dispatch import Signal

# this is what allows us to create the hashtags immediately
# so when a party is created, the hashtags get the signal to register
parsed_hashtags = Signal(providing_args=['hashtag_list'])