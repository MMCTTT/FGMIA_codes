import os

import PIL.Image
from loguru import logger as log
from torch.utils.data import Dataset
from torchvision import transforms


class VGGFace2Dataset(Dataset):
    def __init__(self, root_dir, transform=None, filename="mini1000_1.txt"):
        self.root_dir = root_dir
        self.transform = transform
        if transform is None:
            self.transform = self.getDefaultTransforms()
        self.list_imgs_path = os.path.join(self.root_dir, filename)

        self.list_imgs = []

        if not os.path.exists(self.list_imgs_path):
            log.error("ERROR in readListFile")
            raise FileExistsError(self.list_imgs_path)

        with open(self.list_imgs_path, "r") as f:
            for index, context in enumerate(f):
                context = context.strip()
                one_line = context.split(" ")
                class_id = int(one_line[1])
                img_path = one_line[0]

                self.list_imgs.append(
                    {
                        'cid': class_id,
                        'img': img_path
                    }
                )
                if index % 10000 == 0:
                    log.info("[Dataset]: Processing to Line{}", index)

    def __len__(self):
        return len(self.list_imgs)

    def __getitem__(self, index):
        info = self.list_imgs[index]
        img_path = os.path.join(self.root_dir, "data/", info["img"])
        # log.info("infrx:{} Img:{}, label:{}", index, info['img'], info['cid'])
        img = PIL.Image.open(img_path)
        if self.transform is not None:
            img = self.transform(img)
        return img, info['cid']

    def getDefaultTransforms(self):
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])


if __name__ == "__main__":
    log.info("Hello, World!")
    root_dir = os.path.expanduser("~/dataset/vggface2")
    dataset = VGGFace2Dataset(root_dir, filename="mini1000_1.txt")
    log.info("datalen :{}", len(dataset))
    image, label = dataset[0]
    # 给图像处理后到文件test.png
    preprocess = transforms.Compose([
        transforms.Normalize(mean=[-1, -1, -1], std=[2, 2, 2]),  # 反归一化
        transforms.ToPILImage(),
    ])

    # 将张量应用预处理转换
    image = preprocess(image)
    image.save("test.png")