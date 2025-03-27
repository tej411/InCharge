import RPi.GPIO as GPIO
import time

class ESC:
    def __init__(self, pin, min_value, max_value, arm_value):
        """
        Initialize ESC with specific parameters
        
        :param pin: GPIO pin number
        :param min_value: Minimum PWM value
        :param max_value: Maximum PWM value
        :param arm_value: Arming PWM value
        """
        self.pin = pin
        self.min_value = min_value
        self.max_value = max_value
        self.arm_value = arm_value
        
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
        # Create PWM object
        self.pwm = GPIO.PWM(self.pin, 50)  # 50 Hz frequency
        self.pwm.start(0)
    
    def arm(self):
        """
        Arm the ESC by sending the arm value
        """
        self.pwm.ChangeDutyCycle(self._value_to_duty_cycle(self.arm_value))
        time.sleep(1)
    
    def speed(self, value):
        """
        Set ESC speed
        
        :param value: Speed value between min_value and max_value
        """
        # Ensure value is within allowed range
        value = max(self.min_value, min(self.max_value, value))
        self.pwm.ChangeDutyCycle(self._value_to_duty_cycle(value))
    
    def _value_to_duty_cycle(self, value):
        """
        Convert PWM value to duty cycle
        
        :param value: PWM value
        :return: Duty cycle percentage
        """
        # Convert 1000-2000 microsecond range to 2-12% duty cycle
        return (value - 1000) * (12 - 2) / (2000 - 1000) + 2

def main():
    # LED Pin (using GPIO number, not board pin)
    LED_PIN = 17  # This should be adjusted to match your actual GPIO setup
    
    # Disable GPIO warnings
    GPIO.setwarnings(False)
    
    try:
        # Setup LED
        GPIO.setup(LED_PIN, GPIO.OUT)
        
        # Create ESC objects
        M1 = ESC(pin=10, min_value=1000, max_value=2000, arm_value=1500)
        M2 = ESC(pin=11, min_value=1000, max_value=2000, arm_value=1500)
        
        # Arm ESCs
        M1.arm()
        M2.arm()
        
        # Turn on LED to indicate arming
        GPIO.output(LED_PIN, GPIO.HIGH)
        
        # Wait for system to stabilize
        time.sleep(5)
        
        # Main control loop
        while True:
            # Set constant speed (similar to original code)
            M1.speed(1580)
            M2.speed(1580)
            
            time.sleep(0.015)  # 15 millisecond delay
    
    except KeyboardInterrupt:
        # Clean up on keyboard interrupt
        print("Stopping ESCs")
    
    finally:
        # Cleanup GPIO
        M1.pwm.stop()
        M2.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
