#!/bin/sh
# Build cputhrottle_<version>_all.deb with plain dpkg-deb (no debhelper needed).
set -e
VERSION=$(sed -n 's/^APP_VERSION = "\(.*\)"/\1/p' cputhrottle)
ROOT=build/deb/cputhrottle_${VERSION}_all
rm -rf build/deb && mkdir -p "$ROOT/DEBIAN" dist
install -Dm755 cputhrottle          "$ROOT/usr/bin/cputhrottle"
install -Dm755 cputhrottle-helper   "$ROOT/usr/libexec/cputhrottle-helper"
install -Dm644 cputhrottle.desktop  "$ROOT/usr/share/applications/cputhrottle.desktop"
install -Dm644 org.cputhrottle.policy "$ROOT/usr/share/polkit-1/actions/org.cputhrottle.policy"
install -Dm644 cputhrottle-init.service    "$ROOT/usr/lib/systemd/system/cputhrottle-init.service"
install -Dm644 cputhrottle-sampler.service "$ROOT/usr/lib/systemd/system/cputhrottle-sampler.service"
install -Dm644 cpudb.csv "$ROOT/usr/share/cputhrottle/cpudb.csv"
install -Dm644 cputhrottle.svg "$ROOT/usr/share/icons/hicolor/scalable/apps/cputhrottle.svg"
install -Dm644 LICENSE "$ROOT/usr/share/doc/cputhrottle/copyright"

cat > "$ROOT/DEBIAN/control" <<CTL
Package: cputhrottle
Version: ${VERSION}
Architecture: all
Maintainer: WiiPro38 <wiipro@local>
Section: utils
Priority: optional
Depends: python3, python3-gi, python3-gi-cairo, python3-cairo, gir1.2-gtk-3.0, pkexec | policykit-1
Recommends: gir1.2-ayatanaappindicator3-0.1, pciutils
Homepage: https://github.com/WiiPro38/cputhrottle-linux
Description: Control CPU performance, power limits and sensors
 Lightweight Python/GTK3 app to control CPU governors, frequency, Turbo Boost,
 power limits (PL1/PL2) and platform profile, with live CPU/GPU temperature and
 wattage sensors and a light/dark theme. Privileged changes go through polkit,
 so no sudo is needed. Personal, non-commercial use only; no redistribution
 (see /usr/share/doc/cputhrottle/copyright).
CTL

cat > "$ROOT/DEBIAN/postinst" <<'SH'
#!/bin/sh
set -e
if [ -d /run/systemd/system ]; then
    systemctl daemon-reload || true
    # CPU watts need root-only RAPL counters on modern kernels
    systemctl enable --now cputhrottle-sampler.service || true
    # applies the saved profile at boot (does nothing until auto-switching is enabled in the app)
    systemctl enable cputhrottle-init.service || true
fi
gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
exit 0
SH
cat > "$ROOT/DEBIAN/prerm" <<'SH'
#!/bin/sh
set -e
if [ -d /run/systemd/system ] && { [ "$1" = remove ] || [ "$1" = purge ]; }; then
    systemctl disable --now cputhrottle-sampler.service || true
    systemctl disable cputhrottle-init.service || true
fi
exit 0
SH
cat > "$ROOT/DEBIAN/postrm" <<'SH'
#!/bin/sh
set -e
[ -d /run/systemd/system ] && systemctl daemon-reload || true
gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
exit 0
SH
chmod 755 "$ROOT/DEBIAN/postinst" "$ROOT/DEBIAN/prerm" "$ROOT/DEBIAN/postrm"

dpkg-deb --build --root-owner-group "$ROOT" "dist/cputhrottle_${VERSION}_all.deb"
echo "Built dist/cputhrottle_${VERSION}_all.deb"
