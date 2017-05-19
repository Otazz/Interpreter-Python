INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __str__(self):
		return 'Token({type}, {value})'.format(
			type = self.type,
			value = repr(self.value)
		)

	def __repr__(self):
		return self.__str__()

class Interpreter(object):
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.current_token = None

	def error(self):
		raise Exception('Error parsing input')

	def get_next_token(self):
		text = self.text

		if self.pos > len(text) - 1:
			return Token(EOF, None)

		current_char = text[self.pos]

		if current_char.isdigit():
			token = Token(INTEGER, int(current_char))
			self.pos += 1
			return token

		if current_char == '+':
			token = Token(PLUS, current_char)
			self.pos += 1
			return token

		if current_char == '-':
			token = Token(MINUS, current_char)
			self.pos += 1
			return token	

		if current_char == " ":
			self.pos += 1
			return self.get_next_token()

		self.error()

	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.current_token = self.get_next_token()
		else:
			self.error()

	def expr(self):
		left = ""
		right = ""
		self.current_token = self.get_next_token()

		while self.current_token.type == INTEGER:
			left = left + str(self.current_token.value)
			self.eat(INTEGER)

		op = self.current_token
		if op.type == 'PLUS' or op.type == 'MINUS':
			self.eat(op.type)
		else:
			self.error()

		while self.current_token.type == INTEGER:
			right = right + str(self.current_token.value)
			self.eat(INTEGER)
		if op.type == 'PLUS':
			result = int(left) + int(right)
		else:
			result = int(left) - int(right)
		return result

	def test(self, token):
		return token.type == INTEGER or token.type == PLUS

def main():
	while True:
		try:
			text = raw_input('calc> ')
		except EOFError:
			break
		if not text:
			continue
		interpreter = Interpreter(text)
		result = interpreter.expr()
		print(result)

if __name__ == '__main__':
	main()