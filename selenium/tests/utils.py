import sys

def get_domain():
	if len(sys.argv) > 2 and '-' not in sys.argv[2]:
		 domain = "https://" + sys.argv[2]
	else:
		 domain = "http://localhost:8000"
	print("Domain to test: " + domain)
	return domain