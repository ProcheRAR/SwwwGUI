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
source=(".")
sha256sums=('SKIP')

prepare() {
  cd "${srcdir}"
  # Compile GResource file
  python compile_resources.py
  
  # Исправляем предупреждения в setup.py
  sed -i 's/find_packages/find_namespace_packages/g' setup.py
}

build() {
  cd "${srcdir}"
  python setup.py build
}

package() {
  cd "${srcdir}"
  python setup.py install --root="$pkgdir" --optimize=1 --skip-build
  
  # Install desktop file
  install -Dm644 data/swwwgui.desktop "$pkgdir/usr/share/applications/swwwgui.desktop"
  
  # Install icon
  install -Dm644 data/icons/swwwgui.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/swwwgui.svg"
  
  # Install license
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  
  # Удаляем файлы для разработки, чтобы оставить только необходимое для работы
  rm -rf "$pkgdir"/usr/lib/python*/site-packages/swwwgui-*.egg-info
} 