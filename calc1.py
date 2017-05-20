INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'
MULTIPLY, DIVIDE = 'MULTIPLY', 'DIVIDE'

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
		self.current_char = self.text[self.pos]

	def error(self):
		raise Exception('Error parsing input')

	def advance(self):
		self.pos += 1
		if self.pos > len(self.text) - 1:
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]

	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	def integer(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.advance()
		return int(result)

	def get_next_token(self):
		while self.current_char is not None:
			if self.current_char.isspace():
				self.skip_whitespace()
				continue

			if self.current_char.isdigit():
				return Token(INTEGER, self.integer())

			if self.current_char == '+':
				self.advance()
				return Token(PLUS, '+')

			if self.current_char == '-':
				self.advance()
				return Token(MINUS, '-')

			if self.current_char == '*':
				self.advance()
				return Token(MULTIPLY, '*')

			if self.current_char == '/':
				self.advance()
				return Token(DIVIDE, '/')

			self.error()
		
	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.current_token = self.get_next_token()
		else:
			self.error()

	def expr(self):
		result = 0
		self.current_token = self.get_next_token()

		left = self.current_token
		self.eat(INTEGER)
		result = left.value

		while self.current_token is not None:
			op = self.current_token
			if op.type == 'PLUS':
				self.eat(PLUS)
			elif op.type == 'MINUS':
				self.eat(MINUS)
			elif op.type == 'MULTIPLY':
				self.eat(MULTIPLY)
			else:
				self.eat(DIVIDE)

			right = self.current_token
			self.eat(INTEGER)

			if op.type == 'PLUS':
				result += right.value
			elif op.type == 'MINUS':
				result -= right.value
			elif op.type == 'MULTIPLY':
				result *= right.value
			else:
				result /= right.value
		return result

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