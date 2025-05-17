# global variables start

# dictionary of npcs Key = name values = greeting, I am statement
npcs = {"Guy": ("Greetings", "I am"), "Aldith": ("Hello", "I am"), "Rowan": ("Good morning", "I am"),
        "Borin": ("Hi", "I am"), "Pierre": ("Bonjour", "je suis"), "Dora": ("Hola", "me llamo"),
        "Emperor Chu": ("Ni hao", "Wo jao"), "not important": ("Ah", "my name is"),
        "Aleixo-Defender of man": ("Olá", "meu nome é")}

# sword dictionary Key = name values = minimum damage, maxium damage, damage multiplier
weapons = {"sword": (1, 3, 1), "fists": (0, 2, 1), "axe": (0, 3, 2), "spear": (3, 4, 1), "hammer": (2, 8, 1),
           "tentacle": (0, 1, 10)}

# boss dictionary Key = name values = description, health
bosses = {"King of Bananas": (
    "leader of the monkeys", 5, ["finds an opening and jumps on you", "you get squashed in the process"]),
    "Litius": ("pincher of men", 6, ["Litius opens his pincer and grabs you", "you have been crushed"]),
    "squid": ("creator of storms", 8, ["waves his tentacle and slaps you", "you fly into the sea unconscious"])}

# inventory (starting with fists)
inventory = ["fists"]

# Keep track of number of fires lit
fires_lit = 0

# open a file called story.txt and write in it
myfile = open("story.txt", 'w')

# global variables end