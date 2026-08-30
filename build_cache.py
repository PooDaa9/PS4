#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
باتش لإنشاء ملف cache.appcache تلقائياً
يقوم بمسح المجلد واستثناء بعض الملفات
"""

import os
import sys
import hashlib
from datetime import datetime

# ============================================================
# الإعدادات - عدل هنا حسب احتياجك
# ============================================================

# الملفات والمجلدات اللي مش عاوزها تدخل في الكاش
EXCLUDE_EXTENSIONS = {'.py', '.pyc', '.git', '.DS_Store', '.appcache', '.swp', '.tmp'}
EXCLUDE_FILES = {'cache.appcache', 'sw.js', 'README.md', '.gitignore'}
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules'}

# الملفات الأساسية اللي لازم تكون في الكاش (حتى لو مش موجودة)
CORE_FILES = [
    'index.html',
    'run_lapse.html',
    'PS4_13.00_Webkit.html',
    'sysctl.html',
    'preview.png',
    'chain_lapse.js',
    'chain_poops.js',
    'sysctl.js'
]

# ============================================================
# الوظائف
# ============================================================

def get_all_files(directory='.'):
    """جلب كل الملفات في المجلد مع استثناءات"""
    files = []
    
    for root, dirs, filenames in os.walk(directory):
        # استثناء المجلدات المحددة
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for filename in filenames:
            # استثناء الملفات المحددة
            if filename in EXCLUDE_FILES:
                continue
            
            # استثناء الامتدادات المحددة
            ext = os.path.splitext(filename)[1].lower()
            if ext in EXCLUDE_EXTENSIONS:
                continue
            
            # المسار النسبي
            rel_path = os.path.join(root, filename)
            if rel_path.startswith('./'):
                rel_path = rel_path[2:]
            files.append(rel_path)
    
    return files

def generate_cache_manifest(files, output_file='cache.appcache'):
    """توليد ملف cache.appcache"""
    
    # حساب الـ hash للملفات عشان التحديث
    hash_input = ''.join(sorted(files))
    version_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
    
    # وقت التوليد
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    content = f"""CACHE MANIFEST
# Generated: {timestamp}
# Version: {version_hash}
# 
# هذا الملف تم إنشاؤه تلقائياً بواسطة باتش بايثون
# لا تقم بتعديله يدوياً - أي تغيير سيفقد عند إعادة التشغيل

CACHE:
"""
    
    # إضافة الملفات الأساسية أولاً
    for core in CORE_FILES:
        if core in files:
            content += f"{core}\n"
            files.remove(core)
        else:
            content += f"# {core} (غير موجود)\n"
    
    # إضافة باقي الملفات
    for f in sorted(files):
        content += f"{f}\n"
    
    # إضافة الشبكة (السماح بكل شيء)
    content += """
NETWORK:
*
"""
    
    # إضافة صفحة الفشل (اختياري)
    content += """
FALLBACK:
/ /offline.html
"""
    
    # كتابة الملف
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ تم إنشاء {output_file}")
    print(f"   • عدد الملفات: {len(files) + len(CORE_FILES)}")
    print(f"   • الإصدار: {version_hash}")
    print(f"   • الوقت: {timestamp}")
    
    return content

def check_pages():
    """التحقق من وجود الصفحات الأساسية"""
    missing = []
    for page in ['index.html', 'run_lapse.html', 'PS4_13.00_Webkit.html', 'sysctl.html']:
        if not os.path.exists(page):
            missing.append(page)
    
    if missing:
        print("⚠️  تحذير: الملفات التالية غير موجودة:")
        for m in missing:
            print(f"   • {m}")
        print("   هل أنت في المجلد الصحيح؟")
        return False
    return True

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("  🚀  منشئ cache.appcache التلقائي")
    print("=" * 50)
    print()
    
    # التحقق من المجلد
    if not check_pages():
        print()
        response = input("هل تريد المتابعة على أي حال؟ (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # جلب الملفات
    print("📂 جاري مسح المجلد...")
    files = get_all_files()
    print(f"   • تم العثور على {len(files)} ملف")
    print()
    
    # توليد الملف
    generate_cache_manifest(files)
    print()
    
    # عرض محتوى الملف (اختياري)
    show = input("هل تريد عرض محتوى الملف؟ (y/n): ")
    if show.lower() == 'y':
        print("\n" + "=" * 50)
        print("محتوى cache.appcache:")
        print("=" * 50)
        with open('cache.appcache', 'r', encoding='utf-8') as f:
            print(f.read())
    
    print("\n✅ تم الانتهاء بنجاح!")
    print("📌 تذكر: أي تغيير في الملفات يتطلب إعادة تشغيل الباتش")
    print("   عشان يتم تحديث الإصدار (version hash)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ تم الإلغاء بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        sys.exit(1)