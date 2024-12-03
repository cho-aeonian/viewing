import RPi.GPIO as GPIO
import time

# GPIO 및 스텝 모터 핀 설정
step_pins_can = [5, 6, 13, 19]
for pin in step_pins_can:
    GPIO.setup(pin, GPIO.OUT)

step_pins_open = [17, 27, 22, 10]
for pin in step_pins_open:
    GPIO.setup(pin, GPIO.OUT)

step_pins_plastic = [1, 7, 8, 25]
for pin in step_pins_plastic:
    GPIO.setup(pin, GPIO.OUT)

# IN1, IN2 핀 설정 (vinyl)
IN1 = 20
IN2 = 21
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# 스텝 모터 시퀀스 설정
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# 스텝 모터 동작 함수
def step_motor_with_steps(step_pins, steps, delay, direction='forward'):
    sequence = step_sequence if direction == 'forward' else step_sequence[::-1]
    for _ in range(steps):
        for step in sequence:
            for pin in range(4):
                GPIO.output(step_pins[pin], step[pin])
            time.sleep(delay)
    for pin in step_pins:
        GPIO.output(pin, False)

# 라벨에 따른 동작 수행 함수
def perform_action_based_on_label(label):
    steps_per_revolution = 128
    steps_per_revolution1 = 256

    if label == 'vinyl':
        step_motor_with_steps(step_pins_open, steps_per_revolution, 0.001, direction='forward')
        time.sleep(2)
        step_motor_with_steps(step_pins_open, steps_per_revolution, 0.001, direction='reverse')
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        time.sleep(5)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)

    elif label == 'plastic':
        step_motor_with_steps(step_pins_open, steps_per_revolution, 0.001, direction='forward')
        time.sleep(2)
        step_motor_with_steps(step_pins_open, steps_per_revolution, 0.001, direction='reverse')
        time.sleep(1)
        step_motor_with_steps(step_pins_plastic, steps_per_revolution1, 0.001, direction='reverse')
        time.sleep(1)
        step_motor_with_steps(step_pins_plastic, steps_per_revolution1, 0.001, direction='forward')

    elif label == 'can':
        step_motor_with_steps(step_pins_open, steps_per_revolution, 0.001, direction='forward')
        time.sleep(2)
        step_motor_with_steps(step_pins_open, steps_per_revolution, 0.001, direction='reverse')
        time.sleep(1)
        step_motor_with_steps(step_pins_can, steps_per_revolution1, 0.001, direction='forward')
        time.sleep(1)
        step_motor_with_steps(step_pins_can, steps_per_revolution1, 0.001, direction='forward')

    elif label == 'general':
        step_motor_with_steps(step_pins_open, steps_per_revolution, 0.001, direction='forward')
        time.sleep(1)
        step_motor_with_steps(step_pins_open, steps_per_revolution, 0.001, direction='reverse')
