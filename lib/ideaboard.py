from machine import Pin, PWM, ADC
from neopixel import NeoPixel

class IdeaBoard:
    def __init__(self, m1a=12, m1b=14, m2a=13, m2b=15):
        self._pixel_pin = Pin(2, Pin.OUT)
        self._brightness = 0.5
        self._np = NeoPixel(self._pixel_pin, 1)
        self._np[0] = (0,0,0)
        self._m1a = PWM(Pin(m1a))
        self._m1b = PWM(Pin(m1b))
        self._m2a = PWM(Pin(m2a))
        self._m2b = PWM(Pin(m2b))
    
    def pixel(self, color=(0,0,0)):
        r,g,b = color
        r = int(r * self._brightness)
        g = int(g * self._brightness)
        b = int(b * self._brightness)
        color = (r,g,b)
        #print('color',color)
        self._np[0] = color
        self._np.write()
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, new_brightness):
        if new_brightness <= 1 or new_brightness >= 0:
            self._brightness = new_brightness
    
    def arcoiris(self, n=0):
        color = self._wheel(n)
        self.pixel(color)
    
    def motor_1(self, vel=0):
        if vel < -1023 | vel > 1023:
            print(f"velocidad no valida: {vel}")
        if vel >= 0:
            self._m1a.duty(vel)
            self._m1b.duty(0)
        if vel < 0:
            self._m1a.duty(0)
            self._m1b.duty(vel * -1)
    
    def motor_2(self, vel=0):
        if vel < -1023 | vel > 1023:
            print(f"velocidad no valida: {vel}")
        if vel >= 0:
            self._m2a.duty(vel)
            self._m2b.duty(0)
        if vel < 0:
            self._m2a.duty(0)
            self._m2b.duty(vel * -1)
    
    def _wheel(self, pos):
        # Adafruit color wheel code
        # Input a value 0 to 255 return RGB tuple.
        if pos < 0:
            return (0, 0, 0)
        if pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (int(pos * 3), int(255 - (pos * 3)), 0)
        elif pos < 170:
            pos -= 85
            return (int(255 - pos * 3), 0, int(pos * 3))
        else:
            pos -= 170
            return (0, int(pos * 3), int(255 - pos * 3))
        
    class Servo:
        def __init__(self, pin):
            """
            Initialize the servo

            """
            self._servo = PWM(Pin(pin))
            self._servo.freq(50) # 50Hz for most hobby servos
            
            # Calibrate the servo 1170 y el máximo es 8664
            self._duty_eq = self.calibrate(min_duty = 1170, max_duty = 8664, min_angle = 0, max_angle = 210)
            self.angle(0)
        
        def calibrate(self, min_duty, max_duty, min_angle = 0, max_angle = 180):
            """
            Calibrate the servo range and angle
                        
            """
            self._duty_eq = lambda angle: (angle - min_angle) * (max_duty - min_duty) / (max_angle - min_angle) + min_duty
            return self._duty_eq

        def angle(self, angle):
            """
            Set the angle of the servo.
            
            """

            duty = int(self._duty_eq(angle))
            #print(duty)
            self._servo.duty_u16(duty)
        
        def set_duty(self, duty):
            """
            Manually set the duty cycle of the signal.
            
            """
            self._servo.duty_u16(duty)
            
    class AnalogIn:
        def __init__(self, pin):
            self._pin = ADC(Pin(pin), atten=ADC.ATTN_11DB)
        
        def read(self):
            return self._pin.read()
