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
makedepends=('python-setuptools' 'python-pip' 'python-wheel' 'python-build' 'python-installer')
options=('!emptydirs')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/heads/main.tar.gz")
sha256sums=('SKIP')

prepare() {
  cd "SwwwGUI-main"
  
  # Compile GResource file
  python compile_resources.py
}

build() {
  cd "SwwwGUI-main"
  python -m build --wheel --no-isolation
}

package() {
  cd "SwwwGUI-main"
  python -m installer --destdir="$pkgdir" dist/*.whl
  
  # Install desktop file
  install -Dm644 data/swwwgui.desktop "$pkgdir/usr/share/applications/swwwgui.desktop"
  
  # Install icon
  install -Dm644 data/icons/swwwgui.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/swwwgui.svg"
  
  # Install license
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
} 