#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة الفلاتر - تطبيق الفلاتر على الصور
TikPhoto - Professional Image Editor
Copyright © 2024 Hussein Al-Sokar
"""

from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np


class FilterTool:
    """أداة تطبيق الفلاتر"""
    
    def __init__(self, image):
        self.image = image
        self.filters = {
            'blur': lambda: self.image.filter(ImageFilter.GaussianBlur(radius=2)),
            'sharpen': lambda: self.image.filter(ImageFilter.SHARPEN),
            'edge': lambda: self.image.filter(ImageFilter.FIND_EDGES),
            'emboss': lambda: self.image.filter(ImageFilter.EMBOSS),
            'smooth': lambda: self.image.filter(ImageFilter.SMOOTH_MORE),
            'grayscale': lambda: self.image.convert('L'),
            'sepia': self.apply_sepia,
            'negative': self.apply_negative,
            'vintage': self.apply_vintage,
            'cool': self.apply_cool,
            'warm': self.apply_warm,
        }
    
    def get_available_filters(self):
        """الحصول على قائمة الفلاتر المتاحة"""
        return list(self.filters.keys())
    
    def apply_filter(self, filter_name):
        """تطبيق فلتر محدد"""
        if filter_name in self.filters:
            return self.filters[filter_name]()
        return self.image
    
    def apply_sepia(self):
        """فلتر السيبيا"""
        img = self.image.convert('RGB')
        pixels = np.array(img, dtype=np.float32)
        
        sepia = np.array([[0.393, 0.769, 0.189],
                         [0.349, 0.686, 0.168],
                         [0.272, 0.534, 0.131]])
        
        result = np.zeros_like(pixels)
        for i in range(3):
            result[:, :, i] = np.clip(
                pixels[:, :, 0] * sepia[i, 0] +
                pixels[:, :, 1] * sepia[i, 1] +
                pixels[:, :, 2] * sepia[i, 2],
                0, 255
            )
        
        return Image.fromarray(result.astype('uint8'))
    
    def apply_negative(self):
        """فلتر الصورة السالبة"""
        img = self.image.convert('RGB')
        pixels = np.array(img)
        inverted = 255 - pixels
        return Image.fromarray(inverted.astype('uint8'))
    
    def apply_vintage(self):
        """فلتر عتيق"""
        img = self.image.convert('RGB')
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(0.8)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.7)
        return img
    
    def apply_cool(self):
        """فلتر بارد"""
        img = self.image.convert('RGB')
        pixels = np.array(img, dtype=np.float32)
        pixels[:, :, 2] = np.clip(pixels[:, :, 2] * 1.3, 0, 255)
        pixels[:, :, 0] = np.clip(pixels[:, :, 0] * 0.8, 0, 255)
        return Image.fromarray(pixels.astype('uint8'))
    
    def apply_warm(self):
        """فلتر دافئ"""
        img = self.image.convert('RGB')
        pixels = np.array(img, dtype=np.float32)
        pixels[:, :, 0] = np.clip(pixels[:, :, 0] * 1.3, 0, 255)
        pixels[:, :, 2] = np.clip(pixels[:, :, 2] * 0.8, 0, 255)
        return Image.fromarray(pixels.astype('uint8'))
    
    def apply_black_white(self):
        """فلتر أبيض وأسود"""
        return self.image.convert('L')
    
    def apply_posterize(self, bits=2):
        """فلتر البسترة"""
        return ImageOps.posterize(self.image, bits)
    
    def apply_solarize(self):
        """فلتر التشمس"""
        return ImageOps.solarize(self.image)
