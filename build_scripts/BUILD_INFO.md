# Build Scripts Information

## 🚀 Available Build Scripts

### 1. `build_fast.bat` ⚡ (RECOMMENDED)
**الأسرع - يستبعد الملفات الضخمة غير الضرورية**

- ✅ يستبعد `android-sdk` (حجم ضخم)
- ✅ يستبعد `gradle` (غير ضروري للتشغيل)
- ✅ يستبعد `ApexGamesAPK` (مشروع APK)
- ✅ يتضمن فقط الألعاب والملفات الضرورية
- ⚡ **وقت البناء: ~2-5 دقائق**

**الاستخدام:**
```bash
build_fast.bat
```

---

### 2. `build_portable.bat` 📦
**بناء كامل مع جميع الملفات**

- ⚠️ يتضمن جميع ملفات ApexGames (بما فيها android-sdk)
- ⚠️ حجم أكبر
- ⚠️ **وقت البناء: ~10-20 دقيقة**

**الاستخدام:**
```bash
build_portable.bat
```

---

### 3. `build.bat` 📄
**بناء ملف واحد (Single EXE)**

- ملف تنفيذي واحد فقط
- أبطأ في البدء
- **وقت البناء: ~5-10 دقائق**

**الاستخدام:**
```bash
build.bat
```

---

## 💡 التوصية

استخدم **`build_fast.bat`** للبناء السريع والحجم الأصغر.

الملفات المستبعدة (android-sdk, gradle) مطلوبة فقط لبناء APK للأندرويد، وليست ضرورية لتشغيل التطبيق على Windows.

---

## 🐛 حل مشكلة التأخير

إذا كان البناء بطيئاً جداً:

1. استخدم `build_fast.bat`
2. احذف مجلد `build_scripts\build` قبل البناء
3. تأكد من أن برنامج مكافحة الفيروسات لا يفحص المجلد

---

## 📊 مقارنة الأحجام

| Build Type | Size | Build Time | Includes |
|------------|------|------------|----------|
| Fast       | ~150MB | 2-5 min | Games only |
| Portable   | ~500MB | 10-20 min | Everything |
| Single EXE | ~200MB | 5-10 min | Games only |
