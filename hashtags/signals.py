from django.dispatch import Signal

# this is what allows us to create the hashtags immediately

parsed_hashtags = Signal(providing_args=['hashtag_list'])