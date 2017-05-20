from random import random, choice
from time import sleep

space_character = " "
brick_character = "█"
ruin_characters = ["▞", "▚"]

width = 80
width_change_per_row = 3 # Increase this to make the slope more gradual

prologue = """I met a traveller from an antique land, 
Who said—“Two vast and trunkless legs of stone 
Stand in the desert. . . . Near them, on the sand, 
Half sunk a shattered visage lies, whose frown, 
And wrinkled lip, and sneer of cold command, 
Tell that its sculptor well those passions read 
Which yet survive, stamped on these lifeless things, 
The hand that mocked them, and the heart that fed; 
And on the pedestal, these words appear: 
My name is Ozymandias, King of Kings;"""

legend = [
	"█   ███ ███ █ █    ███ ███   ██ ██ █ █   █   █ ███ ██  █ █ ███   █ █ ███",
	"█   █ █ █ █ █ █    █ █ █ █   █ █ █ █ █   █   █ █ █ █ █ █ █ █     █ █ █  ",
	"█   █ █ █ █ ██     █ █ █ █   █   █  █    █ █ █ █ █ ██  ██  ███    █  ███",
	"█   █ █ █ █ █ █    █ █ █ █   █   █  █    █ █ █ █ █ █ █ █ █   █    █  █  ",
	"███ ███ ███ █ █    ███ █ █   █   █  █    ██ ██ ███ █ █ █ █ ███    █  ███",
    "                                                                        ",
    "   ██ ██ █ ███ █ █ ███ █ █    ███ ███ ██    ██  ███ ███ ███ ███ █ ██    ",
    "   █ █ █ █ █   █ █  █  █ █    █ █ █ █ █ █   █ █ █   █   █ █ █ █ █ █ █   ",
    "   █   █ █ █ █ ███  █   █     █ █ █ █ █ █   █ █ ███ ███ ███ █ █ █ ██    ",
    "   █   █ █ █ █ █ █  █   █     ███ █ █ █ █   █ █ █     █ █   ███ █ █ █   ",
    "   █   █ █ ███ █ █  █   █     █ █ █ █ ██    ██  ███ ███ █   █ █ █ █ █   "
]

epilogue = """Nothing beside remains. Round the decay 
Of that colossal Wreck, boundless and bare 
The lone and level sands stretch far away.”"""

def replace_at(string, index, replacement):
	return string[:index] + replacement + string[index+1:]

class Row:
	def __init__(self, width, image_width):
		self.width = width

		space = image_width - width
		left_space = int(space / 2) * space_character
		bricks = width * brick_character
		self.contents = left_space + bricks

	def weather_brick(self, index):
		current = self.contents[index]
		if current == space_character:
			return

		if current in ruin_characters:
			char = " "
		else:
			char = choice(ruin_characters)
		self.contents = replace_at(self.contents, index, char)

	def weather(self, weathering_rate):
		for i in range(0, len(self.contents)):
			if random() < weathering_rate:
				self.weather_brick(i)

	def render(self):
		print(self.contents)

	def brick_count(self):
		return len(list(b for b in self.contents if b == brick_character))

class Pyramid:
	def __init__(self, width, width_change_per_row):
		self.rows = []
		row_width = 0
		while row_width < width:
			self.rows.append(Row(row_width, width))
			row_width += width_change_per_row

		self.rows.append(Row(0, width))
		legend_width = max(len(line) for line in legend)
		left_space = int((width - legend_width) / 2)
		for line in legend:
			row = Row(0, width)
			row.contents = (space_character * left_space) + line
			self.rows.append(row)

	def render(self):
		for row in self.rows:
			row.render()

	def weather(self, weathering_rate):
		for row in self.rows:
			row.weather(weathering_rate)

	def brick_count(self):
		return sum(r.brick_count() for r in self.rows)

def clear_terminal():
	print(chr(27) + "[2J")

def render_pyramid():
	p = Pyramid(width, width_change_per_row)
	i = 0
	weathering_rate = 0
	while p.brick_count() > 25:	
		weathering_rate += 0.00002
		clear_terminal()
		p.weather(weathering_rate)
		p.render()
		i += 1
		sleep(0.1)

print(prologue)
input("\nPress enter...")
render_pyramid()
print(epilogue)

