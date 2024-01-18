class retinaface(object):
    import PIL
    from ultralytics import YOLO
    from src.convert import convert_to_braille_unicode, parse_xywh_and_class
    def __init__(self, model_name,model_path):
        self.model_path = model_path
        self.model_name =model_name
        # constants
        self.CONF = 0.15 # or other desirable confidence threshold level
        self.MODEL_PATH = "./model_save/yolov8_braille.pt"
        self.IMAGE_PATH = "./assets/alpha-numeric.jpeg"
    def __init__(self):
        self.CONF = 0.15 # or other desirable confidence threshold level
        self.model_path = "./model_save/yolov8_braille.pt"
        self.image_path ="./assets/alpha-numeric.jpeg"
            
    def load_model(self,model_path):
        """load model from path"""
        self.model = YOLO(self.model_path)
        return self.model

    def load_image(image_path):
        """load image from path"""
        image = PIL.Image.open(image_path)
        return image

    def receive_results(self,image_path):
        # receiving results from the model
        image = self.load_image(image_path)
        model = self.load_model(self.model_path)
        res = model.predict(image, save=True, save_txt=True, exist_ok=True, conf=self.CONF)
        boxes = res[0].boxes  # first image
        list_boxes = parse_xywh_and_class(boxes)

        result = ""
        for box_line in list_boxes:
            str_left_to_right = ""
            box_classes = box_line[:, -1]
            for each_class in box_classes:
                str_left_to_right += convert_to_braille_unicode(model.names[int(each_class)])
            result += str_left_to_right + "\n"
        return result
