%{!?_unitdir:%global _unitdir /usr/lib/systemd/system}

Name:           cputhrottle
Version:        1.5.0
Release:        1%{?dist}
Summary:        Control CPU performance and throttling on Linux

License:        Proprietary (personal, non-commercial use only; no redistribution)
URL:            https://github.com/WiiPro38/cputhrottle-linux
BuildArch:      noarch

Source0:        cputhrottle
Source1:        cputhrottle.desktop
Source2:        cputhrottle-helper
Source3:        org.cputhrottle.policy
Source4:        cputhrottle-init.service
Source5:        cputhrottle-sampler.service
Source6:        cpudb.csv
Source7:        cputhrottle.svg
Source8:        LICENSE

Requires:       python3
Requires:       python3-gobject
Requires:       python3-cairo
Requires:       gtk3
Requires:       polkit
Recommends:     libayatana-appindicator-gtk3

%description
A lightweight Python/GTK3 application to control CPU governors, maximum
frequency, Turbo Boost, power limits and platform power profile on Linux,
with live CPU/GPU temperature and wattage sensors and a light/dark theme. Privileged changes
are done through polkit (pkexec), so no sudo or terminal is needed.

%prep
# no sources to unpack

%build
# nothing to build

%install
install -Dm755 %{SOURCE0} %{buildroot}%{_bindir}/cputhrottle
install -Dm755 %{SOURCE2} %{buildroot}%{_libexecdir}/cputhrottle-helper
install -Dm644 %{SOURCE1} %{buildroot}%{_datadir}/applications/cputhrottle.desktop
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/polkit-1/actions/org.cputhrottle.policy
install -Dm644 %{SOURCE4} %{buildroot}%{_unitdir}/cputhrottle-init.service
install -Dm644 %{SOURCE5} %{buildroot}%{_unitdir}/cputhrottle-sampler.service
install -Dm644 %{SOURCE6} %{buildroot}%{_datadir}/cputhrottle/cpudb.csv
install -Dm644 %{SOURCE7} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/cputhrottle.svg
install -Dm644 %{SOURCE8} %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%post
systemctl daemon-reload >/dev/null 2>&1 || :
gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
# CPU watts need root-only RAPL counters on modern kernels: start the tiny sampler
systemctl enable --now cputhrottle-sampler.service >/dev/null 2>&1 || :
# applies the saved profile at boot (does nothing until auto-switching is enabled in the app)
systemctl enable cputhrottle-init.service >/dev/null 2>&1 || :

%preun
if [ "$1" -eq 0 ]; then
    systemctl disable --now cputhrottle-sampler.service >/dev/null 2>&1 || :
    systemctl disable cputhrottle-init.service >/dev/null 2>&1 || :
fi

%postun
systemctl daemon-reload >/dev/null 2>&1 || :

%files
%{_bindir}/cputhrottle
%{_libexecdir}/cputhrottle-helper
%{_datadir}/applications/cputhrottle.desktop
%{_datadir}/polkit-1/actions/org.cputhrottle.policy
%{_unitdir}/cputhrottle-init.service
%{_unitdir}/cputhrottle-sampler.service
%{_datadir}/cputhrottle/cpudb.csv
%{_datadir}/icons/hicolor/scalable/apps/cputhrottle.svg
%license LICENSE

%changelog
* Sat Nov 14 2026 WiiPro <wiipro@local> - 1.5.0-1
- Tray: removed the live temperature badge/text; plain static icon (new cputhrottle icon)
- CPU recognition: more name sources (cpuinfo, lscpu, device tree), cleaner names, more CPU families estimated
- Controls open with the CPU's default values unless the user saved settings; saved settings are per-CPU, kept across restarts and re-applied at boot (optional)
- Settings file: atomic write, backup copy and automatic recovery
- Narrower window with compact tabs and refreshed styling
- License changed to personal non-commercial use, no redistribution; terms added to the privacy policy
* Sat Nov 07 2026 WiiPro <wiipro@local> - 1.4.1-1
- Overview: new "Default vs current settings" panel; modified values are highlighted; "Restore defaults" button
- Compare window: removed the shared filter bar; each of the three boxes is now searchable on its own (type any words, pick from suggestions)
* Sat Nov 07 2026 WiiPro <wiipro@local> - 1.4.0-1
- Expand cpudb.csv to ~180 Intel (7th-14th gen, Core Ultra, N-series) and AMD Ryzen (2000-9000, mobile and desktop) processors
- CPU database panel now uses a teal/cyan style
- Add "Compare processors" window: up to three CPUs side by side with the best value highlighted and a filter box
* Sat Nov 07 2026 WiiPro <wiipro@local> - 1.3.1-1
- Add CPU database (cpudb.csv): power-limit defaults and maxima, clocks, TDP, Tjmax and benchmark scores per CPU
- Power-limit spin boxes and presets never exceed the CPU's rated maxima; warn when current limits are above them
- Add "Add this CPU to my database" button (writes ~/.config/cputhrottle/cpudb.csv)
- Fix boot service: new "apply-boot" helper command finds the real user's saved settings (works for presets too)
- Battery power: ignore peripheral batteries, sum multiple batteries, add unit sanity checks
* Fri Nov 06 2026 WiiPro <wiipro@local> - 1.3.0-1
- Add Sensors tab: CPU/GPU temperatures, live CPU and GPU watts, fans, battery draw, live graphs
- Power-limit defaults now come from the CPU (factory value, RAPL rating or model estimate); add "Use recommended"
- Add Settings tab: dark/light/auto theme, accent colour, version, privacy policy and developer info
- Add temperature in tray (coloured badge and/or text) with configurable colours and thresholds
- Add cputhrottle-sampler service so CPU watts work on kernels where RAPL counters are root-only
* Thu Nov 05 2026 WiiPro <wiipro@local> - 1.2.1-1
- Power limit range now bounded by the CPU declared and original limits; add restore-original button
* Thu Nov 05 2026 WiiPro <wiipro@local> - 1.2.0-1
- Add RAPL power limits (PL1/PL2), platform profile, min frequency, SMT and core count
- Add saved profiles and automatic AC/battery switching
- Tabbed interface

* Thu Nov 05 2026 WiiPro <wiipro@local> - 1.1.0-1
- Rewrite: live per-core frequency and temperature, presets, turbo and EPP
- Privileged changes via polkit helper instead of sudo
- Optional system tray icon

* Thu Nov 05 2026 WiiPro <wiipro@local> - 1.0.0-1
- Initial release of cputhrottle-linux
