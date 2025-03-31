import pyray as ray
import numpy as np

WIN_W = 1600
WIN_H = 900

N_POINTS = 100
SIZE = 10
SPEED = 500 # pixel/s

T_COLOR = ray.ORANGE

class Viz:
    def __init__(self, points: np.ndarray):
        ray.init_window(WIN_W, WIN_H, "Testing QuadTree")
        ray.set_config_flags(ray.FLAG_MSAA_4X_HINT)
        # ray.set_target_fps(60)

        self.timer = 0

        self.points = points
        self.directions: np.ndarray = np.random.randint(-10, 10, size=self.points.shape)/10

    def update(self):
        self.delay = ray.get_frame_time()
        self.timer += self.delay

        for i in range(self.points.shape[0]):
            x = self.points[i, 0]
            y = self.points[i, 1]

            incr = self.directions[i, [0, 1]]

            if (x+incr[0]-SIZE < 0) or (x+incr[0]+SIZE > WIN_W):
                self.directions[i, 0] *= (-1)

            if (y+incr[1]-SIZE < 102) or (y+incr[1]+SIZE > WIN_H):
                self.directions[i, 1] *= (-1)

            self.points[i, 0] += self.directions[i, 0] * self.delay * SPEED
            self.points[i, 1] += self.directions[i, 1] * self.delay * SPEED

    def draw(self):
        ray.begin_drawing()
        ray.clear_background(ray.BLACK)

        rec = ray.Rectangle(0, 0, WIN_W, 94)
        ray.draw_rectangle_pro(rec, (3, 3), 0, ray.DARKGRAY)
        ray.draw_rectangle_lines_ex(rec, 3, ray.ORANGE)

        ray.draw_text("Gas Simulation (i think?)", 11, 11, 36, T_COLOR)
        ray.draw_text(f"Passed time: {self.timer:.1f} | FPS: {ray.get_fps()}", 11, 65, 24, T_COLOR)

        ray.draw_text(f"Num. Particules: {N_POINTS}", 461, 11, 24, T_COLOR)
        ray.draw_text(f"Size: {SIZE}", 461, 38, 24, T_COLOR)
        vel_mean = self.directions.mean(axis=0)
        ray.draw_text(f"Avg Velocity: [{vel_mean[0]*SPEED:.1f}, {vel_mean[1]*SPEED:.1f}]", 461, 65, 24, T_COLOR)

        for i in range(self.points.shape[0]):
            x = self.points[i, 0]
            y = self.points[i, 1]
            ray.draw_circle(x, y, SIZE, ray.WHITE)

        ray.end_drawing()


    def run(self):
        while not ray.window_should_close():
            self.update()
            self.draw()
            ray.draw_fps(10, 10)

        ray.close_window()


if __name__ == "__main__":
    points_x = np.random.randint(102, WIN_W-102, size=N_POINTS).reshape((-1, 1))
    points_y = np.random.randint(102, WIN_H-102, size=N_POINTS).reshape((-1, 1))
    points = np.concatenate((points_x, points_y), axis=1, dtype=np.float32)
    del points_x, points_y

    app = Viz(points)
    app.run()