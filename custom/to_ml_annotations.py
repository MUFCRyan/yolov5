import os
from PIL import Image


root_path = os.path.dirname(__file__).replace('/detection/yolov5/custom', '')
label_path = root_path + '/detection/yolov5/runs/detect/exp/labels/'
label_image_path = root_path + '/detection/yolov5/runs/detect/exp/'
anno_path = root_path + '/dataset/Fires/test/annotations/'
result_path = root_path + '/dataset/Fires/test/result/'


def transform(txt_name, line):
    image_name = str(txt_name).replace('.txt', '') + '.jpg'
    print(line)
    clazz, coor_x, coor_y, coor_width, coor_height, confidence = str(line).split(' ')
    image = Image.open(label_image_path + image_name)
    image_width, image_height = image.size
    image.close()
    coor_x = float(coor_x)
    coor_y = float(coor_y)
    coor_width = float(coor_width)
    coor_height = float(coor_height)
    center_x = image_width * coor_x
    center_y = image_height * coor_y
    width = image_width * coor_width
    height = image_height * coor_height
    ltx = int(center_x - width / 2)
    lty = int(center_y - height / 2)
    rbx = int(center_x + width / 2)
    rby = int(center_y + height / 2)
    file_name = txt_name
    confidence = '{}'.format(float(confidence))
    image_name = image_name.replace('.jpg', '')
    line = '{} {} {} {} {} {}'.format(image_name, str(confidence), str(ltx), str(lty), str(rbx), str(rby))
    print(line)
    return file_name, line

def to_annotations():
    files = os.listdir(label_path)
    results = []
    for file in files:
        if not os.path.isdir(file):
            txt_name = str(file)
            f = open(label_path + file, 'r')
            lines = f.readlines()
            f.close()
            labels = []
            for line in lines:
                file_name, new_line = transform(txt_name, line)
                labels.append(new_line)
                results.append(new_line)
                with open(anno_path + file_name,"w") as f:
                    for label in labels:
                        f.write(label)
                        f.write('\n')
                    f.close()
    f = open(result_path + 'result.txt', 'w')
    for result in results:
        f.write(result)
        f.write('\n')
    f.close()


to_annotations()