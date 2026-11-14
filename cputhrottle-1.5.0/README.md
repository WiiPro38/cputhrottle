# CPU Throttle  ·  التحكم في أداء المعالج

**Version 1.5.0** — Developer: WiiPro38 (NOVAFroge)

A lightweight Python/GTK3 app for Linux to control CPU performance and watch sensors:
governor, frequency range, Turbo Boost, power limits (PL1/PL2), platform profile, SMT and active cores.
Privileged changes go through polkit (`pkexec`) — no `sudo` or terminal needed.

## Features
- Recognises your processor and fills in its **default values** automatically (CPU database of ~340 Intel / AMD models; falls back to RAPL ratings or an estimate from the name).
- Control tab opens with the CPU's defaults, or with **your saved settings** if you saved some. Saved settings are tied to the CPU they were saved on, survive restarts and can be re-applied at startup.
- Overview: temperature, power, clock, battery, per-core frequency, default-vs-current table, CPU database panel and a processor comparison window.
- Sensors: CPU/GPU temperatures and watts, fans, battery draw, live graphs.
- Profiles: Power Saver / Balanced / Performance, your own saved profiles, automatic AC ↔ battery switching.
- Static tray icon with a quick-profile menu; dark / light / auto theme and accent colour.

## Requirements
Python 3, GTK 3 (PyGObject), pycairo, polkit. Optional: Ayatana AppIndicator (tray), `nvidia-smi` (NVIDIA GPU data).

## Install
**Debian / Ubuntu / Mint**
```
sh build-deb.sh            # or: make deb
sudo apt install ./dist/cputhrottle_1.5.0_all.deb
```
**Fedora / openSUSE**
```
make rpm
sudo dnf install ./dist/cputhrottle-1.5.0-*.rpm
```
**Run without installing**
```
make run
```
Tray support: `sudo apt install gir1.2-ayatanaappindicator3-0.1` (Fedora: `libayatana-appindicator-gtk3`).

## Files
| Path | Purpose |
|---|---|
| `~/.config/cputhrottle/settings.json` | your settings (+ `.bak` backup, auto-recovered if damaged) |
| `~/.config/cputhrottle/cpudb.csv` | your own CPU entries (override the system database) |
| `/usr/share/cputhrottle/cpudb.csv` | system CPU database |

Deleting `~/.config/cputhrottle` removes everything the app saved.

## Tips
- **Save & Apply Changes** applies the values and saves them. Use *Forget saved settings* (Settings tab) to go back to the CPU defaults.
- If the orange "currently set in the system" warning stays after applying, the firmware or another power tool (thermald, tlp…) is resetting the limit.
- CPU not in the database? Use *Add this CPU to my database* on the Overview tab and fill in the real values in `cpudb.csv`.

## License
Personal, non-commercial use only. **No commercial use and no redistribution** (including packages, archives and modified copies) without the developer's written permission. Provided "as is", without warranty. See `LICENSE` and the in-app *Privacy Policy & Terms*. The app collects and sends no data.

---

## بالعربية
برنامج خفيف (Python/GTK3) للتحكم في أداء المعالج على لينكس: المتحكّم (governor)، نطاق التردد، Turbo Boost، حدود الطاقة PL1/PL2، وضع الطاقة، SMT وعدد الأنوية، مع مراقبة الحساسات. التغييرات المميّزة تتم عبر polkit دون الحاجة إلى sudo.

**المزايا:** يتعرف على معالجك ويضع قيمه الافتراضية تلقائياً؛ تبويب Control يفتح بالقيم الافتراضية أو بإعداداتك المحفوظة؛ الإعدادات المحفوظة مرتبطة بالمعالج نفسه وتبقى بعد إعادة التشغيل ويمكن تطبيقها عند الإقلاع؛ أيقونة ثابتة في الدرج مع قائمة أنماط سريعة؛ مظهر فاتح/داكن ولون مخصص.

**التثبيت (ديبيان/أوبونتو):** `sh build-deb.sh` ثم `sudo apt install ./dist/cputhrottle_1.5.0_all.deb`. للتجربة دون تثبيت: `make run`.

**الإعدادات:** `~/.config/cputhrottle/settings.json` (مع نسخة احتياطية تُسترجع تلقائياً عند التلف). زر «Forget saved settings» في تبويب Settings يعيد القيم الافتراضية للمعالج.

**الترخيص:** للاستخدام الشخصي غير التجاري فقط. **يُمنع الاستخدام التجاري وإعادة التوزيع** (بما فيها الحزم والأرشيفات والنسخ المعدّلة) دون إذن كتابي من المطوّر. يُقدَّم البرنامج «كما هو» دون ضمان، والبرنامج لا يجمع ولا يرسل أي بيانات.
