from picamera2 import Picamera2
import cv2
from ultralytics import YOLO
import requests
import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# 릴레이 핀 설정
relay_pin = 18
GPIO.setup(relay_pin, GPIO.OUT)

# 첫 번째 스텝 모터 핀 설정 (plastic)
step_pins_1 = [5, 6, 13, 19]
for pin in step_pins_1:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# IN1, IN2 핀 설정 (vinil)
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
def step_motor_with_steps(step_pins, steps, delay):
    for _ in range(steps):
        for step in step_sequence:
            for pin in range(4):
                GPIO.output(step_pins[pin], step[pin])
            time.sleep(delay)
    for pin in step_pins:
        GPIO.output(pin, False)

# YOLO 모델 로드
model = YOLO('best.pt')

# Picamera2 초기화
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
picam2.start()

# URL 설정 (사용 안 함)
# url = 'http://10.150.150.181:5000/label'

try:
    while True:
        # 카메라에서 프레임 읽기
        frame = picam2.capture_array()

        # YOLO 모델에 프레임 전달
        results = model(frame)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # 라벨 가져오기
                label = model.names[int(box.cls)]

                # 사각형과 라벨 표시
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                # 라벨에 따른 동작 수행
                if label in ['mizz_vinil', 'haribo_vinil']:
                    # IN1, IN2 핀 동작
                    GPIO.output(IN1, GPIO.HIGH)
                    GPIO.output(IN2, GPIO.LOW)
                    time.sleep(5)
                    GPIO.output(IN1, GPIO.LOW)
                    GPIO.output(IN2, GPIO.LOW)

                elif label == 'plastic':
                    # 첫 번째 스텝 모터 180도 회전
                    steps_per_revolution = 512
                    step_motor_with_steps(step_pins_1, steps_per_revolution, 0.001)

        # 프레임 표시
        cv2.imshow('viewing', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    GPIO.cleanup()

# Picamera2 종료
picam2.stop()
cv2.destroyAllWindows()
