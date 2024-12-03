from ultralytics import YOLO
import requests
import cv2 as cv

# YOLO 모델 로드
model = YOLO('viewing.pt')

# URL 설정 (Flask 서버에서 label 전송)
label_url = "http://10.150.150.181:8080/label"
auto_url = "http://10.150.150.181:8080/auto-trash"

# 물체 인식 및 그리기 함수 (수동)
def detect_manual(frame):
    results = model(frame)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls)]
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.putText(frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            print(f"label: {label}")

            # 인식된 라벨 전송
            try:
                response = requests.post(label_url, json={"label": label})
                if response.status_code == 200:
                    print("Successfully sent:", response.json())
                else:
                    print("Failed to send label:", response.status_code)
            except Exception as e:
                print("Error sending label:", e)

            # 라벨에 따른 동작 수행
            perform_action_based_on_label(label)
            return  # 한 번 인식한 후 함수 종료

# 자동 물체 인식 함수
def detect_auto(frame):
    results = model(frame)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls)]
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.putText(frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            print(f"label: {label}")

            # 인식된 라벨 전송
            try:
                response = requests.post(auto_url, json={"label": label})
                if response.status_code == 200:
                    print("Successfully sent:", response.json())
                else:
                    print("Failed to send label:", response.status_code)
            except Exception as e:
                print("Error sending label:", e)

            # 라벨에 따른 동작 수행
            perform_action_based_on_label(label)
            return  # 한 번 인식한 후 함수 종료
