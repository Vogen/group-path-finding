import matplotlib.pyplot as plt

from solver import Solver

COLORS = {
    'start': [103, 116, 130],
    'target': [173, 216, 230],
}
for k in COLORS: COLORS[k] = [c / 255. for c in COLORS[k]]

MAX_INT = 10000

fig, ax = plt.subplots()

plt.xlim( -5 , 5 )
plt.ylim( -5 , 5 )

start = [
    [ -1 ,  3],
    [  0 ,  3],
    [  2 ,  0],
]

target = [
    [  3 ,  0],
    [  0 ,  0],
    [ -3 ,  0],
]


start = [
    [  0 ,  3],
    [ -1 ,  3],
    [  1 ,  0],
]

target = [
    [  3 ,  0],
    [  0 ,  0],
    [ -3 ,  0],
]



solver = Solver()
match, cost = solver.solve(start, target)

def draw_points(points, color):
    for p in points:
        circle = plt.Circle(p, 0.2, color=color)
        ax.add_artist(circle)

def draw_match(match):
    for _, e in match.items():
        plt.plot([e.s.x, e.t.x], [e.s.y, e.t.y])

draw_points(start, COLORS['start'])
draw_points(target, COLORS['target'])
draw_match(match)
print('cost', cost)
print('best', 13)

ax.set_aspect( 1 )
plt.title( 'Group Path Finding' )
plt.show()