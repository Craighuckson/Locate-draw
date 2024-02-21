#constants.py

HEIGHT: int = 60  # height of drawing window
WIDTH: int = 70  # width of drawing window

# the four values correspond to values of points on a line (x1,y1,x2,y2)
ECURB: list = [WIDTH // 3, HEIGHT * (0.067), WIDTH // 3, HEIGHT * (0.933)]
WCURB: list = [(WIDTH*2)//3, HEIGHT*0.067, (WIDTH*2)//3, HEIGHT*0.933]
NCURB: list = [WIDTH*(1/WIDTH), (HEIGHT*2)//3, WIDTH*69/WIDTH, (HEIGHT*2)/3] # type: ignore
SCURB: list = [WIDTH*(1/WIDTH), HEIGHT//3, WIDTH-2, HEIGHT//3]

HNCURB: list = [NCURB[0], SCURB[1] + (HEIGHT/15), NCURB[2], SCURB[1] + (HEIGHT/15)]
HSCURB: list = [SCURB[0], NCURB[1] - (HEIGHT/15), NCURB[2], NCURB[1] - (HEIGHT/15)]

# these are x,y (int) coordinates for street text labels
NSTREET: list = [WIDTH / 2, (NCURB[1] + HEIGHT) / 2]
SSTREET: list = [WIDTH / 2, (SCURB[1]) / 2] # type: ignore
WSTREET: list = [(WCURB[0] + WIDTH) / 2, HEIGHT / 2]
ESTREET: list = [ECURB[0] / 2, HEIGHT / 2]
HSTREET: list = [WIDTH / 2, HEIGHT / 2]

#curb labels
HNCURBLABEL: list = [(65/70) * WIDTH, (42/60) * HEIGHT, 12] # x, y , fontsize
HSCURBLABEL: list = [(65/70) * WIDTH, (18/60) * HEIGHT, 12]
WCURBLABEL: list = [(40/70) * WIDTH, (6/60) * HEIGHT, 12]
ECURBLABEL: list = [(22/70) * WIDTH, (6/60) * HEIGHT, 12]


NBLHOUSE1: tuple = (WIDTH*0.10, HEIGHT*0.2, "m") # upper left x, upper left y, house size
NBLHOUSE2: tuple = (WIDTH*0.80, HEIGHT*0.2, "m")
NWBLHOUSE: tuple = (8, 8, "m")
NEBLHOUSE: tuple = (18, 8, "m")
SBLHOUSE1: tuple = (WIDTH*0.1, HEIGHT*0.7, "m")
SBLHOUSE2: tuple = (WIDTH*0.8, HEIGHT*0.7, "m")
SWBLHOUSE: tuple = (9, 16, "m")
SEBLHOUSE: tuple = (16, 16, "m")
WBLHOUSE1: tuple = (WIDTH*0.2, HEIGHT*0.1, "m")
WBLHOUSE2: tuple = (WIDTH*0.2, HEIGHT*0.8, "m")
EBLHOUSE1: tuple = (WIDTH*0.7, HEIGHT*0.1, "m")
EBLHOUSE2: tuple = (WIDTH*0.7, HEIGHT*0.8, "m") # type: ignore

NPLTOPL_DIGBOX = (6, 16, 24, 28)
NWPLTOPL_DIGBOX = (8, 8, 28, 28)
NEPLTOPL_DIGBOX = (4, 8, 24, 28)
SPLTOPL_DIGBOX = (6, 2, 24, 14)
SWPLTOPL_DIGBOX = (9, 3, 27, 22)
SEPLTOPL_DIGBOX = (3, 3, 22, 22)
WPLTOPL_DIGBOX = (14, 6, 28, 24)
EPLTOPL_DIGBOX = (2, 2, 15, 28)

N_DW1 = ()
N_DW2 = ()
S_DW1 = ()
S_DW2 = ()
W_DW1 = ()
W_DW2 = ()
E_DW1 = ()
E_DW2 = ()
NW_DW = ()
NE_DW = ()
SW_DW = ()
SE_DW = ()
