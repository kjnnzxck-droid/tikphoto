#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة النصوص - إضافة وتنسيق النصوص
TikPhoto - Professional Image Editor
Copyright © 2024 Hussein Al-Sokar
"""

from PIL import Image, ImageDraw, ImageFont


class TextTool:
    """أداة إضافة النصوص إلى الصور"""
    
    def __init__(self, image):
        self.image = image
    
    def add_text(self, text, position, font_size=30, color=(255, 255, 255), 
                 font_path=None, opacity=1.0):
        """إضافة نص إلى الصورة"""
        img = self.image.copy()
        draw = ImageDraw.Draw(img, 'RGBA')
        
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        if len(color) == 3:
            color = (*color, int(255 * opacity))
        else:
            color = (*color[:3], int(color[3] * opacity))
        
        draw.text(position, text, font=font, fill=color)
        return img
    
    def add_text_with_shadow(self, text, position, font_size=30, 
                            color=(255, 255, 255), shadow_color=(0, 0, 0),
                            shadow_offset=3):
        """إضافة نص مع ظل"""
        img = self.image.copy()
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except:
            font = ImageFont.load_default()
        
        shadow_pos = (position[0] + shadow_offset, position[1] + shadow_offset)
        draw.text(shadow_pos, text, font=font, fill=shadow_color)
        draw.text(position, text, font=font, fill=color)
        return img
    
    def add_text_centered(self, text, font_size=30, color=(255, 255, 255),
                         y_offset=None):
        """إضافة نص في المركز"""
        img = self.image.copy()
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        
        if y_offset:
            y = y_offset
        
        draw.text((x, y), text, font=font, fill=color)
        return img
    
    def add_watermark(self, watermark_text, position='bottom-right',
                     font_size=20, opacity=0.5):
        """إضافة علامة مائية"""
        img = self.image.convert('RGBA')
        watermark = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark)
        
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        positions = {
            'top-left': (10, 10),
            'top-right': (img.width - text_width - 10, 10),
            'bottom-left': (10, img.height - text_height - 10),
            'bottom-right': (img.width - text_width - 10, img.height - text_height - 10),
            'center': ((img.width - text_width) // 2, (img.height - text_height) // 2)
        }
        
        pos = positions.get(position, positions['bottom-right'])
        
        alpha = int(255 * opacity)
        draw.text(pos, watermark_text, font=font, fill=(255, 255, 255, alpha))
        
        return Image.alpha_composite(img, watermark).convert('RGB')
    
    def add_text_outline(self, text, position, font_size=30, 
                        text_color=(255, 255, 255), outline_color=(0, 0, 0),
                        outline_width=2):
        """إضافة نص مع حدود"""
        img = self.image.copy()
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except:
            font = ImageFont.load_default()
        
        for x_offset in [-outline_width, 0, outline_width]:
            for y_offset in [-outline_width, 0, outline_width]:
                if x_offset != 0 or y_offset != 0:
                    draw.text(
                        (position[0] + x_offset, position[1] + y_offset),
                        text, font=font, fill=outline_color
                    )
        
        draw.text(position, text, font=font, fill=text_color)
        return img
