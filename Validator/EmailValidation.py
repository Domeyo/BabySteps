#does all froms of email validations
import re

def validateFormat(email):
	pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]+$"
	if re.match(pattern, email):
		return True
	return False


