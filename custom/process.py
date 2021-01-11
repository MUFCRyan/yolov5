import os
from PIL import Image
import shutil


root_path = os.path.dirname(__file__).replace('detection/yolov5/custom', '') + 'dataset/Fires/'
test_path = root_path + 'test'
test_image_path = test_path + '/images/'
train_path = root_path + 'train'
train_anno_path = train_path + '/annotations/'
train_image_path = train_path + '/images/'
val_path = root_path + 'val'
val_anno_path = val_path + '/annotations/'
val_image_path = val_path + '/images/'

def split():
    val_anno_files = os.listdir(val_anno_path)
    val_count = len(val_anno_files)
    if val_count > 0: #代表已经划分过，不再划分
        return
    test_images_files = os.listdir(test_image_path)
    train_anno_files = os.listdir(train_anno_path)
    split = 0.1 #取 10% 为验证集
    test_count = len(test_images_files)
    train_count = len(train_anno_files)
    split_count = int((train_count + test_count) * split)
    print('test_count = ' + str(test_count))
    print('train_count = ' + str(train_count))
    print('split_count = ' + str(split_count))
    for index in range(train_count - 1, train_count - split_count, -1):
        label_file = train_anno_files[index]
        image_file_name = str(label_file).replace('.txt', '') + '.jpg'
        old_label_pos = train_anno_path + label_file
        new_label_pos = val_anno_path + label_file
        shutil.move(old_label_pos, new_label_pos)
        old_image_pos = train_image_path + image_file_name
        new_image_pos = val_image_path + image_file_name
        shutil.move(old_image_pos, new_image_pos)


anno_path = ''
label_path = ''
image_path = ''


def transform(process, line):
    image_path = root_path + process + '/images/'
    file_name, clazz, ltx, lty, rbx, rby = str(line).split(' ')
    image = Image.open(image_path + file_name)
    image_width, image_height = image.size
    image.close()
    file_name = file_name.replace('.jpg','')
    ltx = int(ltx)
    lty = int(lty)
    rbx = int(rbx)
    rby = int(rby)
    width = rbx - ltx
    height = rby - lty
    coor_x = (ltx + width/2) / image_width
    coor_y = (lty + height/2) / image_height
    coor_width = width / image_width
    coor_height = height / image_height
    line = '0 ' + str(coor_x) + ' ' + str(coor_y) + ' ' + str(coor_width) + ' ' + str(coor_height)
    return file_name, line

def to_labels(process):
    anno_path = root_path + process + '/annotations/'
    label_path = root_path + process + '/labels/'
    files = os.listdir(anno_path)
    for file in files:
        if not os.path.isdir(file):
            f = open(anno_path + file, 'r')
            lines = f.readlines()
            f.close()
            labels = []
            for line in lines:
                file_name, new_line = transform(process, line)
                labels.append(new_line)
                with open(label_path + file_name + '.txt',"w") as f:
                    for label in labels:
                        f.write(label)
                        f.write('\n')
                    f.close()


def pre_process():
    print('-------------------------------------------')
    split()
    to_labels('train')
    to_labels('val')


pre_process()

