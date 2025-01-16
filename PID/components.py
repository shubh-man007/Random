# components.py
import math

class Proportional:
    def __init__(self, k_p):
        self.k_p = k_p

    def __call__(self, error):
        return error * self.k_p

class Integral:
    def __init__(self, k_i):
        self.k_i = k_i
        self.accumulated_error = 0

    def __call__(self, error):
        self.accumulated_error += error
        # Add a windup limit to prevent excessive integration
        self.accumulated_error = max(min(self.accumulated_error, 10), -10)
        return self.accumulated_error * self.k_i

class Derivative:
    def __init__(self, k_d):
        self.k_d = k_d
        self.last_error = 0

    def __call__(self, error):
        d_error = error - self.last_error
        self.last_error = error
        return d_error * self.k_d

class PID:
    def __init__(self, set_point, k_p, k_i, k_d):
        self.set_value = set_point
        self.proportional = Proportional(k_p)
        self.integral = Integral(k_i)
        self.derivative = Derivative(k_d)

    def __call__(self, error):
        p = self.proportional(error)
        i = self.integral(error)
        d = self.derivative(error)
        output = p + i + d
        return output

class LineFollowingRobot:
    def __init__(self, k_p, k_i, k_d, set_point, base_speed):
        self.pid = PID(set_point, k_p, k_i, k_d)
        self.position = [100, 300]
        self.angle = 0
        self.base_speed = base_speed

    def calculate_error(self, left_sensor, right_sensor):
        return right_sensor - left_sensor  # Reversed for correct steering direction

    def update_position(self, error):
        # Get PID output for steering adjustment
        steering = self.pid(error)
        
        # Limit the steering to prevent excessive rotation
        steering = max(-0.05, min(0.05, steering))
        
        # Update angle and position
        self.angle += steering
        
        # Keep angle between -pi and pi
        self.angle = math.atan2(math.sin(self.angle), math.cos(self.angle))
        
        # Update position based on current angle
        self.position[0] += self.base_speed * math.cos(self.angle)
        self.position[1] += self.base_speed * math.sin(self.angle)

    def simulate_sensors(self, line_data):
        # Simulate sensors with smaller offset
        left_sensor = 1.0 if line_data.is_on_line(self.position, offset=(-3, 0)) else 0.0
        right_sensor = 1.0 if line_data.is_on_line(self.position, offset=(3, 0)) else 0.0
        return left_sensor, right_sensor