Проект хранится в папке (архиве) RelOpt
написанный мною код с подробными комментариями находится в питоновских файлах в IA (Immune Algorithm)

В шаблоне были переделаны файлы, чтобы немного преобразить внешний вид и выбор по умолчанию, а так же добавить опцию выбора моего алгоритма:
    1) function retranslateUi in GUI.Windows.ui_MainWindow.py
    2) function setupUi in GUI.Windows.ui_MainWindow.py
(измненения находятся по единственным комментариям)

Так же в шаблоне были изменены файлы
    1) function LoadAlgConf in MainWindow class in MainWindow.py file
    2) function Run in MainWindow class in MainWindow.py file
Чтобы проект подхватывал мой алгоритм и класс для его инициализации
(изменения находятся по комментариям)

В шаблоне было выдано несколько конфигураций для системы - для каждой из них был создан файл с конфигурациями рассчёта этой системы (в целом настройки отличаются не сильно)
Результат сохранён в файл csv
Все файлы имеют именна похожие:
2014_421_Vasilenko_IAalg_...
2014_421_Vasilenko_IAalg_result_...
2014_421_Vasilenko_IAalg_system_...

моё эссе:
2014_421_Vasilenko_esse.txt

В статье была ссылка на другую статью, где указывался правильный способ для мутаций, там нету чисел, но есть алгоритм
2014_421_Vasilenko_Mutation_Crossing_The Clonal Selection Algorithm with Engineering Applications