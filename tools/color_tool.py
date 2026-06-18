#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة الألوان - تصحيح وتعديل الألوان
TikPhoto - Professional Image Editor
Copyright © 2024 Hussein Al-Sokar
"""

from PIL import Image, ImageEnhance, ImageOps
import numpy as np


class ColorTool:
    """أداة معالجة وتصحيح الألوان"""
    
    def __init__(self, image):
        self.image = image
    
    def adjust_brightness(self, factor):
        """تعديل السطوع (1.0 = عادي، >1 = أفتح، <1 = أغمق)"""
        enhancer = ImageEnhance.Brightness(self.image)
        return enhancer.enhance(factor)
    
    def adjust_contrast(self, factor):
        """تعديل التباين (1.0 = عادي)"""
        enhancer = ImageEnhance.Contrast(self.image)
        return enhancer.enhance(factor)
    
    def adjust_saturation(self, factor):
        """تعديل التشبع (1.0 = عادي، >1 = مشبع، <1 = أقل تشبع)"""
        enhancer = ImageEnhance.Color(self.image)
        return enhancer.enhance(factor)
    
    def adjust_sharpness(self, factor):
        """تعديل الحدة (1.0 = عادي، >1 = حاد، <1 = ناعم)"""
        enhancer = ImageEnhance.Sharpness(self.image)
        return enhancer.enhance(factor)
    
    def auto_contrast(self):
        """تعديل التباين تلقائياً"""
        return ImageOps.autocontrast(self.image)
    
    def auto_color(self):
        """تصحيح الألوان تلقائياً"""
        return ImageOps.autocontrast(self.image.convert('RGB'))
    
    def posterize(self, bits=4):
        """تقليل عدد الألوان"""
        return ImageOps.posterize(self.image, bits)
    
    def solarize(self, threshold=128):
        """تأثير التشمس"""
        return ImageOps.solarize(self.image, threshold)
    
    def equalize_histogram(self):
        """معادلة الهيستوجرام"""
        return ImageOps.equalize(self.image)
    
    def adjust_temperature(self, temperature=0):
        """تعديل درجة الحرارة (دافئ/بارد)"""
        img = self.image.convert('RGB')
        pixels = np.array(img, dtype=np.float32)
        
        if temperature > 0:  # أكثر دفئاً (أحمر/أصفر)
            pixels[:, :, 0] = np.clip(pixels[:, :, 0] * (1 + temperature / 100), 0, 255)
            pixels[:, :, 1] = np.clip(pixels[:, :, 1] * (1 + temperature / 200), 0, 255)
        else:  # أكثر برودة (أزرق)
            pixels[:, :, 2] = np.clip(pixels[:, :, 2] * (1 - temperature / 100), 0, 255)
        
        return Image.fromarray(np.uint8(pixels))
    
    def adjust_highlights(self, factor):
        """تعديل المناطق المضاءة"""
        img = self.image.convert('RGB')
        pixels = np.array(img, dtype=np.float32)
        
        mask = pixels > 128
        pixels[mask] = np.clip(pixels[mask] * factor, 0, 255)
        
        return Image.fromarray(np.uint8(pixels))
    
    def adjust_shadows(self, factor):
        """تعديل المناطق المظلمة"""
        img = self.image.convert('RGB')
        pixels = np.array(img, dtype=np.float32)
        
        mask = pixels < 128
        pixels[mask] = np.clip(pixels[mask] * factor, 0, 255)
        
        return Image.fromarray(np.uint8(pixels))
    
    def invert_colors(self):
        """عكس الألوان"""
        return ImageOps.invert(self.image.convert('RGB'))
    
    def grayscale(self):
        """تحويل إلى رمادي"""
        return self.image.convert('L')
    
    def color_balance(self, red=1.0, green=1.0, blue=1.0):
        """موازنة الألوان"""
        img = self.image.convert('RGB')
        pixels = np.array(img, dtype=np.float32)
        
        pixels[:, :, 0] = np.clip(pixels[:, :, 0] * red, 0, 255)
        pixels[:, :, 1] = np.clip(pixels[:, :, 1] * green, 0, 255)
        pixels[:, :, 2] = np.clip(pixels[:, :, 2] * blue, 0, 255)
        
        return Image.fromarray(np.uint8(pixels))
