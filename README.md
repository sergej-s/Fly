#Мухоемкость

Сделал на Python 2.7 + PyQt4

https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi

http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe

Тестировал под Windows 8 и Ubuntu 14

-----

Тестовое задание

необходимо разработать приложение на C++ или Python, Qt.

1. Использование QT 5 - обязательно
2. Использование git - будет преимуществом

Приложение должно собираться и работать под linux.
3. Кроссплатформенность Linux-Windows - будет преимуществом

-----

Задание: 

Разработать приложение, моделирующее поведение мух в замкнутом пространстве.

После запуска приложения пользователь задает исходные данные:

1. Размер поля в клетках - MxM
2. Максимальное количество мух помещающееся в одной клетке (мухоемкость) - N
3. Затем, пользователь по одной сажает мух на поле
4. Мухи отличаются степенью врожденной тупости - T

Алгоритм полета мухи:
1. Муха появляется на поле в произвольной клетке с учетом мухоемкости
2. Затем муха выбирает соседнюю клетку, в которую она полетит, время принятия решения определяется врожденной тупостью и не должно превышать T
3. Если в выбранной клетке превышена мухоемкость, то муха остается в своей клетке и опять тупит выбирая куда полететь
4. Если в выбранной клетке мухоемкоть не превышена, то муха мгновенно оказывается в заданной клетке

Обязательные условия:
1. Мухи должны летать асинхронно (т.е. каждая муха летает в своем потоке);
2. По каждой мухе собирается полетная информация: скорость, пробег и возраст;
3. Если возраст превышает T*M - то муха дохнет и остается в последней занимаемой клетке навсегда;
4. Необходимо помечать мертвых мух, чтобы их можно было различать на поле;
5. После нажатия кнопки "Стоп" должна выводиться статистика по каждой мухе: средняя скорость и пробег, сдохла или жива;
6. Муха должна быть иконкой, пример - во вложении (google находит много вариантов).

Дополнительные условия - будут преимуществом:
1. Анимация перемещения мух - приветствуется;
2. Подкрашивать иконку в зависимости от степени тупости мухи;
3. Возможность динамически изменять параметры поля (размер и/или мухоемкость);
4. Индивидуальные прикольные иконки мух - приветствуются;
5. Любые усовершенствования делающие поведение мух более жизненным - приветствуется.
