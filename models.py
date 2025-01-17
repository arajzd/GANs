# CSC 321, Assignment 4
#
# This file contains the models used for both parts of the assignment:
#
#   - DCGenerator       --> Used in the vanilla GAN in Part 1
#   - CycleGenerator    --> Used in the CycleGAN in Part 2
#   - DCDiscriminator   --> Used in both the vanilla GAN and CycleGAN (Parts 1 and 2)
#
# For the assignment, you are asked to create the architectures of these three networks by
# filling in the __init__ methods in the DCGenerator, CycleGenerator, and DCDiscriminator classes.
# Note that the forward passes of these models are provided for you, so the only part you need to
# fill in is __init__.

import pdb
import torch
import torch.nn as nn
import torch.nn.functional as F


def deconv(in_channels, out_channels, kernel_size, stride=2, padding=1, batch_norm=True):
    """Creates a transposed-convolutional layer, with optional batch normalization.
    """
    layers = []
    layers.append(nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, bias=False))
    if batch_norm:
        layers.append(nn.BatchNorm2d(out_channels))
    return nn.Sequential(*layers)


def conv(in_channels, out_channels, kernel_size, stride=2, padding=1, batch_norm=True, init_zero_weights=False):
    """Creates a convolutional layer, with optional batch normalization.
    """
    layers = []
    conv_layer = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride,
                           padding=padding, bias=False)
    if init_zero_weights:
        conv_layer.weight.data = torch.randn(out_channels, in_channels, kernel_size, kernel_size) * 0.001
    layers.append(conv_layer)

    if batch_norm:
        layers.append(nn.BatchNorm2d(out_channels))
    return nn.Sequential(*layers)


class ResnetBlock(nn.Module):
    def __init__(self, conv_dim):
        super(ResnetBlock, self).__init__()
        self.conv_layer = conv(in_channels=conv_dim, out_channels=conv_dim, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        out = x + self.conv_layer(x)
        return out


class CycleGenerator(nn.Module):
    """Defines the architecture of the generator network.
       Note: Both generators G_XtoY and G_YtoX have the same architecture in this assignment.
    """

    def __init__(self, conv_dim=64, init_zero_weights=False):
        super(CycleGenerator, self).__init__()

        ###########################################
        ##   FILL THIS IN: CREATE ARCHITECTURE   ##
        ###########################################

        # 1. Define the encoder part of the generator (that extracts features from the input image)
        self.conv1 = conv(in_channels = 3, out_channels = 16, kernel_size = 4, stride=2, padding=1, batch_norm=True)
        self.conv2 = conv(in_channels = 16, out_channels = 32, kernel_size = 4, stride=2, padding=1, batch_norm=True)
        self.conv3 = conv(in_channels=32, out_channels=64, kernel_size=4, stride=2, padding=1, batch_norm=True)

        # 2. Define the transformation part of the generator
        self.resnet_block = ResnetBlock(64)

        # 3. Define the decoder part of the generator (that builds up the output image from features)
        self.deconv1 = deconv(in_channels = 64, out_channels = 32, kernel_size = 4, stride=2, padding=1, batch_norm=True)
        self.deconv2 = deconv(in_channels = 32, out_channels = 16, kernel_size = 4, stride=2, padding=1, batch_norm=True)
        self.deconv3 = deconv(in_channels=16, out_channels=3, kernel_size=4, stride=2, padding=1, batch_norm=True)


    def forward(self, x):
        """Generates an image conditioned on an input image.

            Input
            -----
                x: BS x 3 x 32 x 32

            Output
            ------
                out: BS x 3 x 32 x 32
        """

        out = F.relu(self.conv1(x))
        out = F.relu(self.conv2(out))
        out = F.relu(self.conv3(out))

        out = F.relu(self.resnet_block(out))

        out = F.relu(self.deconv1(out))
        out = F.relu(self.deconv2(out))
        out = F.tanh(self.deconv3(out))


        return out


class DCDiscriminator(nn.Module):
    """Defines the architecture of the discriminator network.
       Note: Both discriminators D_X and D_Y have the same architecture in this assignment.
    """

    def __init__(self, conv_dim=64):
        super(DCDiscriminator, self).__init__()

        ###########################################
        ##   FILL THIS IN: CREATE ARCHITECTURE   ##
        ###########################################

        self.conv1 = conv(in_channels=3, out_channels=32, kernel_size=4, stride=2, padding=1, batch_norm=True)
        self.conv2 = conv(in_channels=32, out_channels=64, kernel_size=4, stride=2, padding=1, batch_norm=True)
        self.conv3 = conv(in_channels=64, out_channels=128, kernel_size=4, stride=2, padding=1, batch_norm=True)
        self.conv4 = conv(in_channels=128, out_channels=256, kernel_size=4, stride=2, padding=1, batch_norm=True)
        self.conv5 = conv(in_channels=256, out_channels=512, kernel_size=4, stride=2, padding=1, batch_norm=True)
        self.conv6 = conv(in_channels=512, out_channels=1, kernel_size=4, stride=2, padding=0, batch_norm=True)

    def forward(self, x):
        out = F.relu(self.conv1(x))
        out = F.relu(self.conv2(out))
        out = F.relu(self.conv3(out))
        out = F.relu(self.conv4(out))
        out = F.relu(self.conv5(out))

        out = self.conv6(out).squeeze()
        out = F.sigmoid(out)
        return out
