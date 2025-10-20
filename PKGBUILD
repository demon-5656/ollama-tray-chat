# Maintainer: demon-5656 <your-email@example.com>
pkgname=ollama-tray-chat
pkgver=1.0.0
pkgrel=1
pkgdesc="GUI chat client for Ollama with system tray support and command execution"
arch=('x86_64')
url="https://github.com/demon-5656/ollama-tray-chat"
license=('MIT')
depends=('python' 'python-pyqt6' 'python-requests')
makedepends=('git')
source=("$pkgname-$pkgver.tar.gz::https://github.com/demon-5656/ollama-tray-chat/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/$pkgname-$pkgver"
    
    # Установка основного скрипта
    install -Dm755 ollama_tray_chat.py "$pkgdir/usr/bin/$pkgname"
    
    # Установка .desktop файла
    install -Dm644 ollama-tray-chat.desktop "$pkgdir/usr/share/applications/ollama-tray-chat.desktop"
    
    # Установка иконки
    install -Dm644 icons/ollama-chat.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/ollama-chat.svg"
    
    # Установка документации
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
    install -Dm644 QUICKSTART.md "$pkgdir/usr/share/doc/$pkgname/QUICKSTART.md"
    install -Dm644 LICENSE "$pkgdir/usr/share/doc/$pkgname/LICENSE"
}
