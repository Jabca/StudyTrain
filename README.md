# Устный счёт на сечения

Эта программа поможет вам легко генерировать небольшие задания
на построение сечений многогранников или самостоятельно проверить себя
в интерактивном режиме.

## Установка

### Инсталятор
Вы можете скачать установщик для систем Windows из папки dist с этого репозитория.

### Клонирование
Если вы хотите изучить код или использовать программу на Linux, то вы можете выполнть следующие команды.

```zsh
cd <working_directory>
git clone https://github.com/Jabca/StudyTrain
cd StudyTrain
pip install -r requirements
```

## Использование
Запускайте приложение используя приложение, которое вы получили после утановки или через коносль командой.

```zsh
python generate_tasks.py
```
Перед вами появится это окно, оно позволяет выбрать количество заданий, которые вы хотите создать.
(можете использовать стрелочки вверх/вниз на клавиатуре чтобы менять значение)

![number chooser](https://raw.githubusercontent.com/Jabca/StudyTrain/master/gui/source/number_chooser.png?raw=true)


После выбора количества заданий у вас появится окно

![approve window](https://raw.githubusercontent.com/Jabca/StudyTrain/master/gui/source/approve_window.png?raw=true)

Здесь вы проверяете корректность заданий, но и можете менять то, как оно отображается.

- верхний ползунок отвечает за угол под которым видна фигура('+' и '-' на нампаде)
- левый ползунок отвечает за сдвиг фигуры по вертикале(стрелочки вверх и вниз)
- нижний ползунок отвечает за горизонтальное перемещение фигуры(стрелочки вправо и влево)
- зелёная кнопка сохраняет задание (Enter)
- красная кнопка удаляет задание (Esc)

После завершения работы в папке с программой появится папка "res"(если её там до этого не было)

![files](https://raw.githubusercontent.com/Jabca/StudyTrain/master/gui/source/files.png?raw=true)

В ней создастся папка с наванием в формате dd-mm-yy_hh-mm-ss время берется в момент начала работы программы.

![res folder contents](https://raw.githubusercontent.com/Jabca/StudyTrain/master/gui/source/res_folder.png?raw=true)

В ней содержатся версии для печати для учеников и учителя в формате docx, такого вида.

![docx result](https://raw.githubusercontent.com/Jabca/StudyTrain/master/gui/source/docx_res.png?raw=true)

А также папки с иходными картинками из которых составляены версии для печати.

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[dill]: <https://github.com/joemccann/dillinger>
[git-repo-url]: <https://github.com/joemccann/dillinger.git>
[john gruber]: <http://daringfireball.net>
[df1]: <http://daringfireball.net/projects/markdown/>
[markdown-it]: <https://github.com/markdown-it/markdown-it>
[Ace Editor]: <http://ace.ajax.org>
[node.js]: <http://nodejs.org>
[Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
[jQuery]: <http://jquery.com>
[@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
[express]: <http://expressjs.com>
[AngularJS]: <http://angularjs.org>
[Gulp]: <http://gulpjs.com>

[PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
[PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
[PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
[PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
[PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
[PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
