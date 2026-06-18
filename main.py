#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikPhoto - Professional Image Editor for Android
Copyright © 2024 Hussein Al-Sokar
All rights reserved.
"""

import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
import threading

# استيراد الأدوات
from tools.image_processor import ImageProcessor
from tools.crop_tool import CropTool
from tools.filter_tool import FilterTool
from tools.effects_tool import EffectsTool
from tools.text_tool import TextTool
from tools.color_tool import ColorTool

# تعيين حجم النافذة
Window.size = (540, 960)
Window.title = 'TikPhoto - محرر الصور الاحترافي'


class HomeScreen(Screen):
    """شاشة البداية الرئيسية"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # رأس التطبيق
        header = BoxLayout(size_hint_y=0.2, orientation='vertical')
        title = Label(
            text='📸 TikPhoto',
            font_size='48sp',
            bold=True,
            color=(0.2, 0.6, 1, 1)
        )
        subtitle = Label(
            text='محرر الصور الاحترافي',
            font_size='18sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        header.add_widget(title)
        header.add_widget(subtitle)
        layout.add_widget(header)
        
        # منطقة الأيقونة
        icon_layout = BoxLayout(size_hint_y=0.25)
        camera_icon = Label(
            text='📷',
            font_size='120sp'
        )
        icon_layout.add_widget(camera_icon)
        layout.add_widget(icon_layout)
        
        # أزرار الخيارات
        buttons_layout = GridLayout(cols=2, spacing=15, size_hint_y=0.4)
        
        # زر فتح الصورة
        btn_open = Button(
            text='📁\nفتح صورة',
            background_color=(0.2, 0.6, 1, 1),
            font_size='16sp'
        )
        btn_open.bind(on_press=self.open_image)
        buttons_layout.add_widget(btn_open)
        
        # زر التقط صورة
        btn_capture = Button(
            text='📷\nالتقط صورة',
            background_color=(0.3, 0.8, 0.3, 1),
            font_size='16sp'
        )
        btn_capture.bind(on_press=self.capture_image)
        buttons_layout.add_widget(btn_capture)
        
        # زر المعرض
        btn_gallery = Button(
            text='🖼️\nالمعرض',
            background_color=(1, 0.6, 0.2, 1),
            font_size='16sp'
        )
        btn_gallery.bind(on_press=self.open_gallery)
        buttons_layout.add_widget(btn_gallery)
        
        # زر الإعدادات
        btn_settings = Button(
            text='⚙️\nالإعدادات',
            background_color=(0.8, 0.2, 0.8, 1),
            font_size='16sp'
        )
        btn_settings.bind(on_press=self.open_settings)
        buttons_layout.add_widget(btn_settings)
        
        layout.add_widget(buttons_layout)
        
        # التذييل
        footer = BoxLayout(size_hint_y=0.15, orientation='vertical')
        footer.add_widget(Label(
            text='© 2024 Hussein Al-Sokar | جميع الحقوق محفوظة',
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1)
        ))
        footer.add_widget(Label(
            text='TikPhoto v1.0.0',
            font_size='10sp',
            color=(0.4, 0.4, 0.4, 1)
        ))
        layout.add_widget(footer)
        
        self.add_widget(layout)
    
    def open_image(self, instance):
        """فتح صورة من الجهاز"""
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(
            filters=['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
        )
        content.add_widget(filechooser)
        
        buttons = BoxLayout(size_hint_y=0.1, spacing=10)
        btn_open = Button(text='فتح')
        btn_cancel = Button(text='إلغاء')
        buttons.add_widget(btn_open)
        buttons.add_widget(btn_cancel)
        content.add_widget(buttons)
        
        popup = Popup(title='اختر صورة', content=content, size_hint=(0.9, 0.9))
        
        def open_selected(btn):
            if filechooser.selection:
                self.manager.get_screen('editor').load_image(filechooser.selection[0])
                self.manager.current = 'editor'
                popup.dismiss()
        
        btn_open.bind(on_press=open_selected)
        btn_cancel.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def capture_image(self, instance):
        """التقط صورة جديدة"""
        popup = Popup(
            title='التقط صورة',
            content=Label(text='ميزة الكاميرا قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def open_gallery(self, instance):
        """فتح معرض الصور"""
        self.manager.current = 'gallery'
    
    def open_settings(self, instance):
        """فتح الإعدادات"""
        popup = Popup(
            title='الإعدادات',
            content=Label(text='الإعدادات\n\nالإصدار: 1.0.0\nالمطور: حسين السكر\n© 2024 جميع الحقوق محفوظة'),
            size_hint=(0.8, 0.4)
        )
        popup.open()


class EditorScreen(Screen):
    """شاشة تحرير الصور"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'editor'
        self.current_image_path = None
        self.image_processor = ImageProcessor()
        
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # منطقة عرض الصورة
        self.image_widget = Image()
        main_layout.add_widget(self.image_widget)
        
        # شريط الأدوات
        tools_scroll = ScrollView(size_hint_y=0.25)
        tools_layout = GridLayout(cols=4, spacing=10, size_hint_x=1, size_hint_y=None)
        tools_layout.bind(minimum_height=tools_layout.setter('height'))
        
        tools = [
            ('✂️', 'قص', self.open_crop),
            ('🔄', 'تدوير', self.open_rotate),
            ('📄', 'حجم', self.open_resize),
            ('☀️', 'السطوع', self.open_brightness),
            ('🎨', 'ألوان', self.open_colors),
            ('✨', 'فلاتر', self.open_filters),
            ('⭐', 'تأثيرات', self.open_effects),
            ('📝', 'نص', self.open_text),
            ('🖌️', 'رسم', self.open_draw),
            ('📖', 'إطار', self.open_frame),
            ('💾', 'حفظ', self.save_image),
            ('🔙', 'رجوع', self.go_back),
        ]
        
        for icon, label, callback in tools:
            btn = Button(
                text=f'{icon}\n{label}',
                size_hint_y=None,
                height=80,
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_press=callback)
            tools_layout.add_widget(btn)
        
        tools_scroll.add_widget(tools_layout)
        main_layout.add_widget(tools_scroll)
        
        self.add_widget(main_layout)
    
    def load_image(self, image_path):
        """تحميل صورة للتحرير"""
        self.current_image_path = image_path
        self.image_widget.source = image_path
    
    def open_crop(self, instance):
        popup = Popup(
            title='قص الصورة',
            content=Label(text='أداة القص قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_rotate(self, instance):
        popup = Popup(
            title='تدوير الصورة',
            content=Label(text='أداة التدوير قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_resize(self, instance):
        popup = Popup(
            title='تغيير حجم الصورة',
            content=Label(text='أداة تغيير الحجم قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_brightness(self, instance):
        popup = Popup(
            title='تعديل السطوع والتباين',
            content=Label(text='أداة السطوع قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_colors(self, instance):
        popup = Popup(
            title='تصحيح الألوان',
            content=Label(text='أداة الألوان قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_filters(self, instance):
        popup = Popup(
            title='الفلاتر',
            content=Label(text='أداة الفلاتر قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_effects(self, instance):
        popup = Popup(
            title='التأثيرات',
            content=Label(text='أداة التأثيرات قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_text(self, instance):
        popup = Popup(
            title='إضافة نص',
            content=Label(text='أداة النص قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_draw(self, instance):
        popup = Popup(
            title='الرسم',
            content=Label(text='أداة الرسم قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def open_frame(self, instance):
        popup = Popup(
            title='إضافة إطار',
            content=Label(text='أداة الإطار قيد التطوير\n(قريباً متوفرة)'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def save_image(self, instance):
        popup = Popup(
            title='حفظ الصورة',
            content=Label(text='تم حفظ الصورة بنجاح!'),
            size_hint=(0.8, 0.3)
        )
        popup.open()
    
    def go_back(self, instance):
        """العودة للشاشة الرئيسية"""
        self.manager.current = 'home'


class GalleryScreen(Screen):
    """شاشة معرض الصور"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'gallery'
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text='معرض الصور', size_hint_y=0.1, font_size='24sp')
        layout.add_widget(title)
        
        content = Label(text='المعرض قيد التطوير\n(قريباً متوفر)', size_hint_y=0.8)
        layout.add_widget(content)
        
        btn_back = Button(text='رجوع', size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        
        self.add_widget(layout)


class TikPhotoApp(App):
    """تطبيق TikPhoto الرئيسي"""
    
    def build(self):
        # إنشاء مدير الشاشات
        screen_manager = ScreenManager(transition=NoTransition())
        
        # إضافة الشاشات
        screen_manager.add_widget(HomeScreen())
        screen_manager.add_widget(EditorScreen())
        screen_manager.add_widget(GalleryScreen())
        
        return screen_manager


if __name__ == '__main__':
    app = TikPhotoApp()
    app.run()
