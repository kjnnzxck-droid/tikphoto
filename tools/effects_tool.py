#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة التأثيرات - تطبيق التأثيرات الخاصة
TikPhoto - Professional Image Editor
Copyright © 2024 Hussein Al-Sokar
"""

from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import math


class EffectsTool:
    """أداة التأثيرات الخاصة"""
    
    def __init__(self, image):
        self.image = image
    
    def apply_pixelate(self, pixel_size=10):
        """تأثير البكسلة"""
        img = self.image.resize(
            (self.image.width // pixel_size, self.image.height // pixel_size),
            Image.Resampling.BILINEAR
        )
        return img.resize(self.image.size, Image.Resampling.NEAREST)
    
    def apply_motion_blur(self, size=15):
        """تأثير تمويه الحركة"""
        return self.image.filter(ImageFilter.SMOOTH_MORE)
    
    def apply_vignette(self, strength=0.5):
        """تأثير الزاوية المظلمة"""
        img = self.image.convert('RGB')
        w, h = img.size
        
        vignette = Image.new('L', (w, h), 255)
        vignette_pixels = vignette.load()
        
        for y in range(h):
            for x in range(w):
                dist = ((x - w/2)**2 + (y - h/2)**2)**0.5
                max_dist = ((w/2)**2 + (h/2)**2)**0.5
                factor = 1 - (dist / max_dist) * strength
                vignette_pixels[x, y] = int(255 * max(0, factor))
        
        img.putalpha(vignette)
        return img.convert('RGB')
    
    def apply_lens_flare(self, x=None, y=None, size=50):
        """تأثير توهج العدسة"""
        img = self.image.convert('RGBA')
        if x is None:
            x = img.width // 2
        if y is None:
            y = img.height // 2
        
        flare = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(flare)
        
        for i in range(size, 0, -2):
            alpha = int(100 * (1 - i / size))
            draw.ellipse(
                [x - i, y - i, x + i, y + i],
                fill=(255, 255, 255, alpha)
            )
        
        return Image.alpha_composite(img, flare).convert('RGB')
    
    def apply_oil_painting(self):
        """تأثير الرسم بالزيت"""
        img = self.image.filter(ImageFilter.SMOOTH_MORE)
        return img.filter(ImageFilter.SMOOTH_MORE)
    
    def apply_sketch(self):
        """تأثير الرسم بالقلم"""
        img = self.image.convert('L')
        return img.filter(ImageFilter.FIND_EDGES)
    
    def apply_cartoon(self):
        """تأثير الرسوم المتحركة"""
        img = self.image
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        return img
    
    def apply_mirror_horizontal(self):
        """تأثير المرآة الأفقية"""
        w, h = self.image.size
        img = self.image
        
        mirror_img = Image.new(img.mode, (w * 2, h))
        mirror_img.paste(img, (0, 0))
        mirror_img.paste(img.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (w, 0))
        return mirror_img
    
    def apply_mirror_vertical(self):
        """تأثير المرآة العمودية"""
        w, h = self.image.size
        img = self.image
        
        mirror_img = Image.new(img.mode, (w, h * 2))
        mirror_img.paste(img, (0, 0))
        mirror_img.paste(img.transpose(Image.Transpose.FLIP_TOP_BOTTOM), (0, h))
        return mirror_img
    
    def apply_glitch(self):
        """تأثير الخلل التقني"""
        img = np.array(self.image)
        
        for _ in range(10):
            y = np.random.randint(0, img.shape[0])
            shift = np.random.randint(-20, 20)
            if shift > 0:
                img[y, shift:] = img[y, :-shift]
            else:
                img[y, :shift] = img[y, -shift:]
        
        return Image.fromarray(img.astype('uint8'))
    
    def apply_blur_background(self, blur_amount=15):
        """تأثير تمويه الخلفية"""
        return self.image.filter(ImageFilter.GaussianBlur(radius=blur_amount))
