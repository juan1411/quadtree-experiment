import pyray as ray
import numpy as np

from quadtree import quadTree

WIN_W = 1600
WIN_H = 900

N_POINTS = 1000
SIZE = 1
SPEED = 100 # pixel/s

TANK_W = 1500
TANK_H = 700

T_COLOR = ray.ORANGE
DEV = False

R_POS = (500, 300)
R_SIZE = (200, 200)

class Viz:
    def __init__(self, points: np.ndarray):
        ray.init_window(WIN_W, WIN_H, "Testing QuadTree")
        ray.set_config_flags(ray.FLAG_MSAA_4X_HINT)
        # ray.set_target_fps(60)
        self.timer = 0

        self.points = points
        self.qt: quadTree = None
        self.directions: np.ndarray = None

        # Resolving/starting directions
        if not DEV:
            aa = np.random.randint(-10, 10, size=self.points.shape)/10
        else:
            aa = np.zeros(self.points.shape)

        self.directions = aa.copy()

    def constructing_quadTree(self):
        # Constructing quadTree
        self.qt = None
        self.qt = quadTree(boundaries=(TANK_W, TANK_H), start_pos=(50, 150))
        for i in range(points.shape[0]):
            self.qt.insert(
                (points[i, 0]-SIZE, points[i, 1]-SIZE),
                (2*SIZE, 2*SIZE),
                user_data=(i)
            )

    def update(self):
        self.delay = ray.get_frame_time()
        self.timer += self.delay

        for i in range(self.points.shape[0]):
            x = self.points[i, 0]
            y = self.points[i, 1]

            incr = self.directions[i, [0, 1]] * self.delay * SPEED

            if (x+incr[0]-SIZE < 50) or (x+incr[0]+SIZE > 50+TANK_W):
                self.directions[i, 0] *= (-1)
                self.directions[i, 0] *= 0.98

            if (y+incr[1]-SIZE < 150) or (y+incr[1]+SIZE > 150+TANK_H):
                self.directions[i, 1] *= (-1)
                self.directions[i, 1] *= 0.98

            self.points[i, 0] += self.directions[i, 0] * self.delay * SPEED
            self.points[i, 1] += self.directions[i, 1] * self.delay * SPEED

        self.constructing_quadTree()

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

        at_region = self.qt[(R_POS, R_SIZE)]
        inds = [node.userData for node in at_region if node.userData is not None]
        ray.draw_text(f"Num. of Counts: {len(at_region)}", 811, 12, 24, T_COLOR)
        ray.draw_text(f"Num. at Region: {len(inds)}", 811, 40, 24, T_COLOR)

        vel_mean = self.directions[inds, ].mean(axis=0)
        factor = SPEED * self.delay * 10
        ray.draw_text(f"Avg Velocity: [{vel_mean[0]*factor:.1f}, {vel_mean[1]*factor:.1f}]", 811, 68, 24, T_COLOR)


        ray.draw_text(f"Dev mode: {DEV}", 1389, 68, 24, T_COLOR)


        tank = ray.Rectangle(0, 0, TANK_W, TANK_H)
        ray.draw_rectangle_pro(tank, (-50, -150), 0, ray.SKYBLUE)
        ray.draw_rectangle_lines(50, 150, TANK_W, TANK_H, ray.WHITE)

        # query region
        ray.draw_rectangle(R_POS[0], R_POS[1], R_SIZE[0], R_SIZE[1], (20, 150, 10, 100))

        # for node in self.qt:
        #     pos = node.root.pos
        #     size = node.root.size
            # ray.draw_rectangle_lines(
            #     int(round(pos[0],0)), int(round(pos[1],0)), int(round(size[0],0)), int(round(size[1],0)),
            #     (255, 255, 255, 100),
            # )
            # if node.root.userData:
            #     ray.draw_rectangle(
            #         int(round(pos[0],0)), int(round(pos[1],0)), int(round(size[0],0)), int(round(size[1],0)),
            #         (250, 0, 0, 100),
            #     )

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
    points_x = np.random.randint(low=55+SIZE, high=45-SIZE+TANK_W, size=N_POINTS).reshape((-1, 1))
    points_y = np.random.randint(low=155+SIZE, high=145-SIZE+TANK_H, size=N_POINTS).reshape((-1, 1))
    points = np.concatenate((points_x, points_y), axis=1, dtype=np.float32)
    del points_x, points_y

    app = Viz(points)
    app.run()