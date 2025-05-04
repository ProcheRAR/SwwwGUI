# Установка SwwwGUI из AUR (Arch Linux)

## Автоматическая установка с помощью AUR-хелпера

Если у вас установлен AUR-хелпер (yay, paru, aurman и т.д.), вы можете установить SwwwGUI одной командой:

```bash
# С использованием yay
yay -S swwwgui

# С использованием paru
paru -S swwwgui
```

## Ручная установка из AUR

1. Клонируйте AUR-репозиторий:
   ```bash
   git clone https://aur.archlinux.org/swwwgui.git
   cd swwwgui
   ```

2. Соберите и установите пакет:
   ```bash
   makepkg -si
   ```

## Зависимости

SwwwGUI требует следующие пакеты:
- python
- python-gobject
- gtk4
- libadwaita
- swww (основная программа для установки обоев)

Опционально:
- matugen (для интеграции matugen)

## Запуск после установки

После установки вы можете запустить SwwwGUI из меню приложений или выполнив команду:

```bash
swwwgui
``` 