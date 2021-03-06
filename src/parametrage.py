reward_table = {
    "0": 1,
    "*": 30,
    "@": -50,
    "?": -9,
    "#": 30
}

obstacles = [(2,2),(1, 4),(2, 4),(3, 4),(3, 1),(3, 2),(7, 6),(7, 7),(8, 6),(9,2),(10,2),(9,3),(6, 4),(7, 4),(6, 3),(7, 3),(4, 5),(4, 6),(9, 9),(2,8),(2,9),(3,8),(3,9)]
bonus = []
bonus_bis = [(4,2),(8,7),(6,7)]

color_table = {
   "0": (255,255,255),
   "*": (0,200,0),
   "@": (0,200,0),
   "?": (0,0,255),
   "#": (125,125,125)
}

possible = {
   "up": ["down","right","left"],
   "down": ["up","right","left"],
   "right": ["down","up","left"],
   "left": ["down","right","up"]
}
