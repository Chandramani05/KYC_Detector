import cv2
import numpy as np

class Prprocess:
    def __init__(self, rect_x=5, rect_y=13, sq_x=33, sq_y=33):
        self._rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (rect_x, rect_y))
        self._sq_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (sq_x, sq_y))
        self._height = 600

    def resize(self, image):
        height, width, _ = image.shape
        ratio = self._height / height
        new_width = int(width * ratio)
        return cv2.resize(image, (new_width, self._height))

    def smooth(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.bilateralFilter(gray, 11, 17, 17)

    def find_dark_regions(self, image):
        return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, self._rect_kernel)

    def apply_threshold(self, image):
        x_grad = cv2.Sobel(image, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        x_grad = np.absolute(x_grad)
        min_val, max_val = np.min(x_grad), np.max(x_grad)
        scaled = np.uint8((x_grad - min_val) / (max_val - min_val) * 255)
        x_grad = cv2.morphologyEx(scaled, cv2.MORPH_CLOSE, self._rect_kernel)
        _, thresh = cv2.threshold(x_grad, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, self._sq_kernel)
        thresh = cv2.erode(thresh, None, iterations=4)
        return thresh

    def find_coordinates(self, im_thresh, im_dark):
        contours = cv2.findContours(im_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect = w / float(h)
            cr_width = w / float(im_dark.shape[1])
            if aspect > 5 and cr_width > 0.5:
                px = int((x + w) * 0.03)
                py = int((y + h) * 0.03)
                x, y = x - px, y - py
                w, h = w + (px * 2), h + (py * 2)
                return y, y + h + 10, x, x + w + 10
        return 0, 0, 0, 0

    def crop_area(self, image):
        resized = self.resize(image)
        smoothed = self.smooth(resized)
        dark = self.find_dark_regions(smoothed)
        thresh = self.apply_threshold(dark)
        y1, y2, x1, x2 = self.find_coordinates(thresh, dark)
        cropped_image = image[y1:y2, x1:x2]
        return dark

    def rotate(self, img, theta):
        rows, cols = img.shape[0], img.shape[1]
        image_center = (cols / 2, rows / 2)
        M = cv2.getRotationMatrix2D(image_center, theta, 1)
        abs_cos = abs(M[0, 0])
        abs_sin = abs(M[0, 1])
        bound_w = int(rows * abs_sin + cols * abs_cos)
        bound_h = int(rows * abs_cos + cols * abs_sin)
        M[0, 2] += bound_w / 2 - image_center[0]
        M[1, 2] += bound_h / 2 - image_center[1]
        rotated = cv2.warpAffine(img, M, (bound_w, bound_h), borderValue=(255, 255, 255))
        return rotated
