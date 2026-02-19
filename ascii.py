import cv2
import os
import argparse

ASCII_CHARS = "@WM#8&BHQ NO0DS%?*+=-:!~^`."
WIDTH = 130

os.system(f'mode con: cols={WIDTH} lines=55')

def resize_image(image, new_width=WIDTH):
    height, width = image.shape[:2]
    new_height = int(new_width * (height / width) * 0.55)
    return cv2.resize(image, (new_width, new_height))

def pixels_to_ascii(image):
    chars = [ASCII_CHARS[int(p) * (len(ASCII_CHARS) - 1) // 255] for p in image.flatten()]
    return "".join(chars)

def main(video_path):
    if not os.path.exists(video_path):
        print("Video not found:", video_path)
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Failed to open video")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = resize_image(gray)
        ascii_str = pixels_to_ascii(resized)
        ascii_image = "\n".join([ascii_str[i:i + WIDTH] for i in range(0, len(ascii_str), WIDTH)])
        print("\033[H" + ascii_image)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    input("Press Enter...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASCII video in terminal")
    parser.add_argument("-v", "--video", type=str, required=True,
        help=r"Path to video, for example: C:\Path\To\video.mp4")
    args = parser.parse_args()
    main(args.video)
