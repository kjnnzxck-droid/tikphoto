#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة القص - قص الصور
TikPhoto - Professional Image Editor
Copyright © 2024 Hussein Al-Sokar
"""

from PIL import Image
import numpy as np


class CropTool:
    """أداة قص الصور"""
    
    def __init__(self, image):
        self.image = image
        self.crop_box = None
    
    def set_crop_box(self, left, top, right, bottom):
        """تحديد منطقة القص"""
        self.crop_box = (left, top, right, bottom)
    
    def crop(self):
        """تنفيذ القص"""
        if self.crop_box:
            return self.image.crop(self.crop_box)
        return self.image
    
    def crop_to_ratio(self, ratio_x, ratio_y):
        """قص الصورة حسب نسبة محددة"""
        width, height = self.image.size
        target_width = width
        target_height = int(width * ratio_y / ratio_x)
        
        if target_height > height:
            target_height = height
            target_width = int(height * ratio_x / ratio_y)
        
        left = (width - target_width) // 2
        top = (height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        return self.image.crop((left, top, right, bottom))
    
    def crop_square(self):
        """قص الصورة لتكون مربعة"""
        return self.crop_to_ratio(1, 1)
    
    def crop_to_16_9(self):
        """قص الصورة بنسبة 16:9"""
        return self.crop_to_ratio(16, 9)
    
    def crop_to_4_3(self):
        """قص الصورة بنسبة 4:3"""
        return self.crop_to_ratio(4, 3)
    
    def crop_to_9_16(self):
        """قص الصورة بنسبة 9:16 (عمودي)"""
        return self.crop_to_ratio(9, 16)
    
    def autocrop(self, border_color=(255, 255, 255)):
        """قص الحدود البيضاء تلقائياً"""
        img_array = np.array(self.image)
        
        if len(img_array.shape) == 3:
            mask = np.any(img_array != border_color, axis=2)
        else:
            mask = img_array != border_color[0]
        
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if rows.any() and cols.any():
            ymin, ymax = np.where(rows)[0][[0, -1]]
            xmin, xmax = np.where(cols)[0][[0, -1]]
            return self.image.crop((xmin, ymin, xmax + 1, ymax + 1))
        
        return self.image
