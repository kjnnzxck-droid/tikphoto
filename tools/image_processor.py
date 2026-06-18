#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالج الصور - معالجة والتلاعب بالصور
TikPhoto - Professional Image Editor
Copyright © 2024 Hussein Al-Sokar
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
import os


class ImageProcessor:
    """فئة معالجة الصور الرئيسية"""
    
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.current_image = None
        self.original_image = None
    
    def load_image(self, image_path):
        """تحميل صورة من ملف"""
        try:
            self.original_image = Image.open(image_path)
            self.current_image = self.original_image.copy()
            return True
        except Exception as e:
            print(f"خطأ في تحميل الصورة: {e}")
            return False
    
    def save_image(self, output_path=None):
        """حفظ الصورة"""
        try:
            if output_path is None:
                import time
                output_path = os.path.join(
                    self.output_dir,
                    f'tikphoto_{int(time.time())}.jpg'
                )
            
            if self.current_image:
                self.current_image.save(output_path, 'JPEG', quality=95)
                return output_path
            return None
        except Exception as e:
            print(f"خطأ في حفظ الصورة: {e}")
            return None
    
    def crop(self, left, top, right, bottom):
        """قص الصورة"""
        if self.current_image:
            self.current_image = self.current_image.crop((left, top, right, bottom))
            return True
        return False
    
    def rotate(self, angle):
        """تدوير الصورة"""
        if self.current_image:
            self.current_image = self.current_image.rotate(angle, expand=True)
            return True
        return False
    
    def resize(self, width, height):
        """تغيير حجم الصورة"""
        if self.current_image:
            self.current_image = self.current_image.resize((width, height), Image.Resampling.LANCZOS)
            return True
        return False
    
    def flip_horizontal(self):
        """قلب الصورة أفقياً"""
        if self.current_image:
            self.current_image = self.current_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            return True
        return False
    
    def flip_vertical(self):
        """قلب الصورة عمودياً"""
        if self.current_image:
            self.current_image = self.current_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            return True
        return False
    
    def adjust_brightness(self, factor):
        """تعديل السطوع (1.0 = عادي، >1 = أفتح، <1 = أغمق)"""
        if self.current_image:
            enhancer = ImageEnhance.Brightness(self.current_image)
            self.current_image = enhancer.enhance(factor)
            return True
        return False
    
    def adjust_contrast(self, factor):
        """تعديل التباين"""
        if self.current_image:
            enhancer = ImageEnhance.Contrast(self.current_image)
            self.current_image = enhancer.enhance(factor)
            return True
        return False
    
    def adjust_saturation(self, factor):
        """تعديل التشبع"""
        if self.current_image:
            enhancer = ImageEnhance.Color(self.current_image)
            self.current_image = enhancer.enhance(factor)
            return True
        return False
    
    def adjust_sharpness(self, factor):
        """تعديل الحدة"""
        if self.current_image:
            enhancer = ImageEnhance.Sharpness(self.current_image)
            self.current_image = enhancer.enhance(factor)
            return True
        return False
    
    def apply_blur(self, radius=5):
        """تطبيق تأثير التمويه"""
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.GaussianBlur(radius))
            return True
        return False
    
    def apply_grayscale(self):
        """تحويل الصورة إلى رمادي"""
        if self.current_image:
            self.current_image = self.current_image.convert('L')
            return True
        return False
    
    def apply_sepia(self):
        """تطبيق تأثير سيبيا"""
        if self.current_image:
            img = self.current_image.convert('RGB')
            pixels = img.load()
            
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    r, g, b = pixels[x, y]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    
                    pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))
            
            self.current_image = img
            return True
        return False
    
    def apply_edge_detection(self):
        """كشف الحواف"""
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.FIND_EDGES)
            return True
        return False
    
    def apply_emboss(self):
        """تطبيق تأثير النقش"""
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.EMBOSS)
            return True
        return False
    
    def apply_smooth(self):
        """تنعيم الصورة"""
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.SMOOTH_MORE)
            return True
        return False
    
    def add_text(self, text, position, font_size=30, color=(255, 255, 255)):
        """إضافة نص إلى الصورة"""
        if self.current_image:
            try:
                draw = ImageDraw.Draw(self.current_image)
                draw.text(position, text, fill=color)
                return True
            except Exception as e:
                print(f"خطأ في إضافة النص: {e}")
                return False
        return False
    
    def add_watermark(self, watermark_text, opacity=0.5):
        """إضافة علامة مائية"""
        if self.current_image:
            watermark = Image.new('RGBA', self.current_image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark)
            
            w, h = self.current_image.size
            text = watermark_text
            
            draw.text((w - 150, h - 50), text, fill=(255, 255, 255, int(255 * opacity)))
            
            self.current_image = Image.alpha_composite(
                self.current_image.convert('RGBA'),
                watermark
            ).convert('RGB')
            return True
        return False
    
    def apply_vignette(self):
        """تطبيق تأثير الزاوية المظلمة"""
        if self.current_image:
            img = self.current_image.convert('RGB')
            w, h = img.size
            
            vignette = Image.new('L', (w, h), 255)
            vignette_pixels = vignette.load()
            
            for y in range(h):
                for x in range(w):
                    dist = ((x - w/2)**2 + (y - h/2)**2)**0.5
                    max_dist = ((w/2)**2 + (h/2)**2)**0.5
                    factor = 1 - (dist / max_dist) * 0.5
                    vignette_pixels[x, y] = int(255 * factor)
            
            img.putalpha(vignette)
            self.current_image = img.convert('RGB')
            return True
        return False
    
    def reset(self):
        """إعادة تعيين الصورة للأصل"""
        if self.original_image:
            self.current_image = self.original_image.copy()
            return True
        return False
    
    def get_image_info(self):
        """الحصول على معلومات الصورة"""
        if self.current_image:
            return {
                'size': self.current_image.size,
                'format': self.current_image.format,
                'mode': self.current_image.mode,
                'width': self.current_image.width,
                'height': self.current_image.height
            }
        return None
