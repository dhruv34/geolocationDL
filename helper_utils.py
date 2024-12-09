import os

from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset


class ImageDataset(Dataset):
    def __init__(self, folder_path, max_images_per_folder=1000):
        self.image_paths = []
        self.labels = []
        self.label_map = {}

        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor()
        ])

        if os.path.isdir(folder_path):
            city_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            self.label_map = {folder: idx for idx, folder in enumerate(city_folders)}

            for city_folder in city_folders:
                city_path = os.path.join(folder_path, city_folder)
                print(f"Loading images from: {city_folder}")

                image_count = 0
                for image_file in os.listdir(city_path):
                    if image_file.endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(city_path, image_file)
                        self.image_paths.append(image_path)
                        self.labels.append(self.label_map[city_folder])
                        image_count += 1

                        if image_count >= max_images_per_folder:
                            break

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")

        image = self.transform(image)
        
        label = self.labels[idx]
        
        return image, label

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]
    

class SplitImageDataset(Dataset):
    def __init__(self, image_paths, labels, transform = transforms.Compose([transforms.Resize((128, 128)), transforms.ToTensor()])):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")
        
        image = self.transform(image)
        
        label = self.labels[idx]
        
        return image, label