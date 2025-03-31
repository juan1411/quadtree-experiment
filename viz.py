import pyray as ray
import numpy as np

from quadtree import quadTree, construct_quadtree

WIN_W = 1600
WIN_H = 900

N_POINTS = 100
SIZE = 10
SPEED = 500 # pixel/s

TANK_W = 1500
TANK_H = 700

T_COLOR = ray.ORANGE
DEV = True

class Viz:
    def __init__(self, points: np.ndarray):
        ray.init_window(WIN_W, WIN_H, "Testing QuadTree")
        ray.set_config_flags(ray.FLAG_MSAA_4X_HINT)
        # ray.set_target_fps(60)
        self.timer = 0

        self.points = points
        # self.space = construct_quadtree(points)
        self.directions: np.ndarray = None

        if not DEV:
            aa = np.random.randint(-10, 10, size=self.points.shape)/10
        else:
            aa = np.zeros(self.points.shape)

        self.directions = aa.copy()

    def update(self):
        self.delay = ray.get_frame_time()
        self.timer += self.delay

        for i in range(self.points.shape[0]):
            x = self.points[i, 0]
            y = self.points[i, 1]

            incr = self.directions[i, [0, 1]]

            if (x+incr[0]-SIZE < 50) or (x+incr[0]+SIZE > 50+TANK_W):
                self.directions[i, 0] *= (-1)
                self.directions[i, 0] *= 0.98

            if (y+incr[1]-SIZE < 150) or (y+incr[1]+SIZE > 150+TANK_H):
                self.directions[i, 1] *= (-1)
                self.directions[i, 1] *= 0.98

            self.points[i, 0] += self.directions[i, 0] * self.delay * SPEED
            self.points[i, 1] += self.directions[i, 1] * self.delay * SPEED

    def draw(self):
        ray.begin_drawing()
        ray.clear_background(ray.BLACK)

        rec = ray.Rectangle(0, 0, WIN_W, 100)
        ray.draw_rectangle_pro(rec, (0, 0), 0, ray.DARKGRAY)
        ray.draw_rectangle_lines_ex(rec, 3, ray.ORANGE)

        ray.draw_text("Gas Simulation (i think?)", 11, 12, 36, T_COLOR)
        ray.draw_text(f"Passed time: {self.timer:.1f} | FPS: {ray.get_fps()}", 11, 68, 24, T_COLOR)

        ray.draw_text(f"Num. Particules: {N_POINTS}", 461, 12, 24, T_COLOR)
        ray.draw_text(f"Size: {SIZE}", 461, 40, 24, T_COLOR)
        vel_mean = self.directions.mean(axis=0)
        factor = SPEED * self.delay * 10
        ray.draw_text(f"Avg Velocity: [{vel_mean[0]*factor:.1f}, {vel_mean[1]*factor:.1f}]", 461, 68, 24, T_COLOR)

        ray.draw_text(f"Dev mode: {DEV}", 1389, 68, 24, T_COLOR)


        tank = ray.Rectangle(0, 0, TANK_W, TANK_H)
        ray.draw_rectangle_pro(tank, (-50, -150), 0, ray.SKYBLUE)
        ray.draw_rectangle_lines(50, 150, TANK_W, TANK_H, ray.WHITE)
        for i in range(self.points.shape[0]):
            x = self.points[i, 0]
            y = self.points[i, 1]
            ray.draw_circle(x, y, SIZE, ray.WHITE)

        ray.end_drawing()
        return None

    def run(self):
        while not ray.window_should_close():
            self.update()
            self.draw()

        ray.close_window()


if __name__ == "__main__":
    points_x = np.random.randint(51+SIZE, 49-SIZE+TANK_W, size=N_POINTS).reshape((-1, 1))
    points_y = np.random.randint(151+SIZE, 149-SIZE+TANK_H, size=N_POINTS).reshape((-1, 1))
    points = np.concatenate((points_x, points_y), axis=1, dtype=np.float32)
    del points_x, points_y

    qt = quadTree(boundaries=(TANK_W, TANK_H), start_pos=(50, 150))
    print(qt)

    for i in range(points.shape[0]):
        qt.put((points[i, 0], points[i, 1]))

    print(qt)
    print("Node-0:", qt._node_0)
    print("Node-1:", qt._node_1)
    print("Node-2:", qt._node_2)
    print("Node-3:", qt._node_3)

    # app = Viz(points)
    # app.run()