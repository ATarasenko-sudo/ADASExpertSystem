class DrivingMetricsCalculator:
    def __init__(self):
        self.prev_amp_steer = 0
        self.prev_amp_acc = 0
        self.prev_mean_vel = 0

    def calc_ldv(self, turning, dist_line):
        if not turning and abs(dist_line) <= 0.2:
            return 1
        else:
            return 0

    def calc_amp_steer(self, steer, steer_prev):
        amp = abs(steer - steer_prev)
        mean_amp = (self.prev_amp_steer + amp) / 2
        self.prev_amp_steer = amp
        return mean_amp

    def calc_amp_acc(self, acc, acc_prev):
        amp = abs(acc - acc_prev)
        mean_amp = (self.prev_amp_acc + amp) / 2
        self.prev_amp_acc = amp
        return mean_amp

    def depal_counter(self, brage_pedal_flag):
        if brage_pedal_flag:
            return 1
        else:
            return 0

    def calc_mean_vel(self, rel_vel):
        mean_amp = (rel_vel + self.prev_mean_vel) / 2
        self.prev_mean_vel = rel_vel
        return mean_amp
