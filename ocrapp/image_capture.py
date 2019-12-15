import cv2

class ImageCapture:
    """Handles webcam access and image capture.
    """

    index = 1
    run = True

    def mevent(event, x, y, flags, param) -> None:
        print(">>> Mouse event")
        if event == cv2.EVENT_LBUTTONDOWN:
            ImageCapture.run = False

    def capture_image(self) -> str:
        """Launches webcam window, allows user to capture image, and saves the image as a .jpg file."
        """
        v_capture = cv2.VideoCapture(0)

        frame_is_available, frame = v_capture.read()
        window_name='videoPlayer'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.mevent)
        key = cv2.waitKey(1)
        while frame_is_available and (key != 27):
            cv2.imshow(window_name, frame)
            frame_is_available, frame = v_capture.read()
            key = cv2.waitKey(1) & 255
        v_capture.release()
        cv2.destroyWindow(window_name)
        cv2.waitKey(1)
        img_file_name = "savedImage%s.jpg" % (ImageCapture.index)
        ImageCapture.index += 1
        cv2.imwrite(img_file_name, frame)

        return img_file_name

    def capture(self) -> None:
        print(">>> Close event")
        ImageCapture.run = False
