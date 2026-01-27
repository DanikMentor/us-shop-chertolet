import os
from app import app

# Печатаем для диагностики
print("--- ДИАГНОСТИКА ПУТЕЙ ---")
print(f"Текущая рабочая директория: {os.getcwd()}")
print(f"Папка с шаблонами по мнению Flask: {app.template_folder}")
print(f"Существует ли папка шаблонов? {os.path.exists(app.template_folder)}")

if os.path.exists(app.template_folder):
    print(f"Файлы в папке шаблонов: {os.listdir(app.template_folder)}")
else:
    print("ВНИМАНИЕ: Flask не видит папку templates!")
print("--------------------------")

if __name__ == "__main__":
    app.run(debug=True)