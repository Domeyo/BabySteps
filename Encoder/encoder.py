import base64

def encode(stringValue):
	stringValue = stringValue.encode()
	stringValue = base64.b64encode(stringValue)
	print(stringValue)
	if str(stringValue)[0] == 'b':
		stringValue = str(stringValue)[2:]
	return stringValue.rstrip("'")


if __name__ == "__main__":
	str_val = "123456"
	print(encode(str_val))	
