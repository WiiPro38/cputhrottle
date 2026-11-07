VERSION = $(shell sed -n 's/^APP_VERSION = "\(.*\)"/\1/p' cputhrottle)
SOURCES = cputhrottle cputhrottle-helper cputhrottle.desktop org.cputhrottle.policy cputhrottle-init.service cputhrottle-sampler.service cpudb.csv

all:
	@echo "Targets:  make deb  |  make rpm  |  make packages  |  make install-deb  |  make install-rpm  |  make run"

# ───── Debian / Ubuntu / Mint (.deb) — needs only dpkg-deb ─────
deb:
	sh ./build-deb.sh

install-deb: deb
	sudo apt install -y ./dist/cputhrottle_$(VERSION)_all.deb

# ───── Fedora / RHEL / openSUSE (.rpm) — needs rpmbuild ─────
rpm:
	mkdir -p ~/rpmbuild/SOURCES ~/rpmbuild/SPECS dist
	cp $(SOURCES) ~/rpmbuild/SOURCES/
	rpmbuild -bb cputhrottle.spec
	cp ~/rpmbuild/RPMS/noarch/cputhrottle-$(VERSION)-*.rpm dist/

install-rpm: rpm
	sudo dnf install -y ./dist/cputhrottle-$(VERSION)-*.rpm

packages: deb rpm

# تشغيل للتجربة بدون تثبيت
run:
	CPUTHROTTLE_HELPER=$(CURDIR)/cputhrottle-helper python3 ./cputhrottle

clean:
	rm -rf build dist ~/rpmbuild/RPMS/*/cputhrottle* ~/rpmbuild/SRPMS/cputhrottle*
