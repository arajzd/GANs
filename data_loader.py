import os

import torch
from torch.utils.data import DataLoader

from torchvision import datasets
from torchvision import transforms


def get_emoji_loader(emoji_type, opts):
    """Creates training and test data loaders.
    """
    transform = transforms.Compose([
                    transforms.Scale(opts.image_size),
                    transforms.ToTensor(),
                    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                ])

    train_path = os.path.join('./emojis', emoji_type)
    test_path = os.path.join('./emojis', 'Test_{}'.format(emoji_type))

    train_dataset = datasets.ImageFolder(train_path, transform)
    test_dataset = datasets.ImageFolder(test_path, transform)

    train_dloader = DataLoader(dataset=train_dataset, batch_size=opts.batch_size, shuffle=True, num_workers=opts.num_workers, drop_last=True)
    test_dloader = DataLoader(dataset=test_dataset, batch_size=opts.batch_size, shuffle=False, num_workers=opts.num_workers, drop_last=True)

    return train_dloader, test_dloader

def get_yosemite_loader(season, opts):
    """Creates training and test data loaders.
    """
    transform = transforms.Compose([
                    transforms.Scale(opts.image_size),
                    transforms.ToTensor(),
                    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                ])

    train_path = os.path.join('datasets/summer2winter_yosemite', season)
    test_path = os.path.join('datasets/summer2winter_yosemite', 'Test_{}'.format(season))

    train_dataset = datasets.ImageFolder(train_path, transform)
    test_dataset = datasets.ImageFolder(test_path, transform)

    train_dloader = DataLoader(dataset=train_dataset, batch_size=opts.batch_size, shuffle=True, num_workers=opts.num_workers, drop_last=True)
    test_dloader = DataLoader(dataset=test_dataset, batch_size=opts.batch_size, shuffle=False, num_workers=opts.num_workers, drop_last=True)

    return train_dloader, test_dloader