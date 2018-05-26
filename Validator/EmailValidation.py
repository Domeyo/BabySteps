#does all froms of email validations
import re

def validateFormat(email):
	pattern = r"[\w+]{1,}@[\w+]{1,}\.[\w+]"
	print(email)
	if re.match(pattern, email):
		print("hahaha")
		return True
	return False

if __name__=="__main__":
	email = input('email = ')
	if validateFormat(email):
		print("valid")
	else:
		print("Invalid")
	
