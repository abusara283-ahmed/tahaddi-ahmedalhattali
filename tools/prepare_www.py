#!/usr/bin/env python3
# يحوّل ملف «تحدّي العباقرة» (index.html) إلى مجلد www لتطبيق APK يعمل دون إنترنت.
# الاستخدام: python3 tools/prepare_www.py <مسار index.html> [مجلد المكتبات vendor]
import sys, os, json, shutil
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); www = os.path.join(root, 'www')
s = open(sys.argv[1], encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, ('patch not found', a[:70])
    s = s.replace(a, b)

# المكتبات من داخل التطبيق بدلاً من الإنترنت
rep("'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js'", "'vendor/pdf.min.js'")
rep("'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'", "'vendor/pdf.worker.min.js'")
rep("'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'", "'vendor/qrcode.min.js'")
rep("'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.49.4/dist/umd/supabase.js'", "'vendor/supabase.js'")
# لا حاجة إلى Service Worker داخل التطبيق
rep("if (ONSITE && 'serviceWorker' in navigator", "if (false && ONSITE && 'serviceWorker' in navigator")
# طبقة التوافق: حفظ الملفات والطباعة وزر الرجوع
shim = open(os.path.join(here, 'apk-shim.js'), encoding='utf-8').read()
i = s.rindex('</script>')
s = s[:i] + '\n/* ===== تطبيق أندرويد ===== */\n' + shim + '\n' + s[i:]
rep('</style>\n</head>', '#instBtn{display:none!important}</style>\n</head>')

os.makedirs(www, exist_ok=True)
open(os.path.join(www, 'index.html'), 'w', encoding='utf-8').write(s)
if len(sys.argv) > 2:
    v = os.path.join(www, 'vendor'); os.makedirs(v, exist_ok=True)
    for f in ('pdf.min.js', 'pdf.worker.min.js', 'qrcode.min.js', 'supabase.js'):
        shutil.copy(os.path.join(sys.argv[2], f), os.path.join(v, f))
print('www جاهز:', round(len(s.encode()) / 1024), 'KB')
