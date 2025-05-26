import albumentations as aug
import os
import cv2
import numpy as np
class augment():
    def __init__(self):
        self.transform = aug.Compose([
            aug.HorizontalFlip(p=0.5),
            aug.RandomBrightnessContrast(p=0.5),
            aug.Rotate(limit=15, p=0.5),
            aug.GaussianBlur(blur_limit=3, p=0.3),
            aug.GaussNoise(p=0.3),
        ])

    def augment_image(self, image):
        return self.transform(image=image)['image']
    
    def augment_folder(self,in_dir = "images/Positive/arav"):
        par_dir = os.path.basename(os.path.dirname(in_dir))
        if par_dir == "Positive":
            num_aug = 80 - len(os.listdir(in_dir))
        elif par_dir == "Negative":
            num_aug = 5 - len(os.listdir(in_dir))
        else : 
            raise ValueError("This directory does not exist!")
        aug_per_im = len(os.listdir(in_dir))/num_aug
        for image_name in os.listdir(in_dir):
            if image_name.lower().endswith(('.jpg','.png','.jpeg')):
                augmented = 0
                i = 0
                image_path = os.path.join(in_dir, image_name)
                image = cv2.imread(image_path)
                try:
                    while i < aug_per_im and augmented < num_aug:
                        augmented = self.augment_image(image)
                        save_path = os.path.join(in_dir, f"{image_name}_aug{i}.jpg")
                        cv2.imwrite(augmented, save_path)
                        i, augmented += 1
                except:
                    print("Image is unavailable/corrupted")
                    continue
            else:
                continue
    def main(self):
        self.augment_folder()
        #get the directory we want to augment images in
        #check if the directory is positive or negative samples
            #if positive, check if folder has atleast 80 images, 
                #if not, make images till it is 80,
                #if yes, continue
            #if negative, check if folder has 5 images,
                #if not, make images till 5,
                #if yes, continue
        #no need to return anything, directories updated while pictures are augmented.
if __name__ == "__main__":
    obj = augment()
    obj.main()
