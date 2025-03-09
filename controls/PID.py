class PID:

    def __init__(self, K_P, K_I, K_D, dt,OUTPUT_MIN,OUTPUT_MAX):
        self.K_P = K_P
        self.K_I = K_I
        self.K_D = K_D
        self.dt = dt
        self.error_previous = 0
        self.integral = 0
        self.OUTPUT_MIN = OUTPUT_MIN
        self.OUTPUT_MAX = OUTPUT_MAX

    def update(self,error):

        P = self.K_P * error

        I = self.integral + self.K_I * error * self.dt

        D = self.K_D * (error - self.error_previous) / self.dt

        self.error_previous = error

        MV = P + I + D

        if MV >= self.OUTPUT_MAX:
            return self.OUTPUT_MAX
        
        elif MV <= self.OUTPUT_MIN:
            return self.OUTPUT_MIN
        
        else:
            self.integral = I
            return MV