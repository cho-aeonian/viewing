import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# 릴레이 핀 설정
relay_pin = 18
GPIO.setup(relay_pin, GPIO.OUT)

# 릴레이 제어 함수
def control_relay(state, delay=None):
    if state == 'on':
        GPIO.output(relay_pin, GPIO.HIGH)
        if delay:
            time.sleep(delay)
    elif state == 'off':
        GPIO.output(relay_pin, GPIO.LOW)

# 예시: 릴레이 사용 예시
def example_usage():
    # 릴레이 ON 상태로 설정 (1.5초 대기 후 OFF)
    control_relay('on', delay=1.5)
    control_relay('off')
    
    # 다른 동작 후 릴레이 ON 상태로 설정 (3.5초 대기 후 OFF)
    control_relay('on', delay=3.5)
    control_relay('off')
