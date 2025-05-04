# Maintainer: ProcheRAR <your-email@example.com>

pkgname=swwwgui
pkgver=1.0.0
pkgrel=1
pkgdesc="A modern GTK4 GUI for swww wallpaper daemon with matugen integration"
arch=('any')
url="https://github.com/ProcheRAR/SwwwGUI"
license=('GPL3')
depends=('python' 'python-gobject' 'gtk4' 'libadwaita' 'swww')
optdepends=('matugen: for matugen theme generation')
makedepends=('python-setuptools' 'python-pip' 'python-wheel')
options=('!emptydirs')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/heads/main.tar.gz")
sha256sums=('SKIP')

prepare() {
  cd "SwwwGUI-main"
  
  # Compile GResource file
  python compile_resources.py
  
  # Fix warnings in setup.py
  sed -i 's/find_packages/find_namespace_packages/g' setup.py
}

build() {
  cd "SwwwGUI-main"
  python setup.py build
}

package() {
  cd "SwwwGUI-main"
  python setup.py install --root="$pkgdir" --optimize=1 --skip-build
  
  # Install desktop file
  install -Dm644 data/swwwgui.desktop "$pkgdir/usr/share/applications/swwwgui.desktop"
  
  # Install icon
  install -Dm644 data/icons/swwwgui.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/swwwgui.svg"
  
  # Install license
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  
  # Remove development files
  rm -rf "$pkgdir"/usr/lib/python*/site-packages/swwwgui-*.egg-info
} 