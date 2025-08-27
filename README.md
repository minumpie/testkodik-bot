# 📦 TestKodik v1.3.0

TestKodik — это телеграм-бот для генерации штрихкодов **Code128** в формате **PNG** по введённому числовому коду товара.

Проект:
- Упакован в **Docker
- Снабжён **Python-** и **Java**-тестами
- Автоматически разворачивается через **Jenkins Pipeline**

<p align="center">
  <img src="images/banner.png" alt="TestKodik Bot" width="250" style="border-radius:25px;"/>
</p>

<p align="center">
  <img src="images/python.png" alt="Python" width="50"/>
  <img src="images/docker.png" alt="Docker" width="50"/>
  <img src="images/telegram.png" alt="Telegram" width="50"/>
  <img src="images/jenkins.png" alt="Jenkins" width="50"/>
</p>


---

## ✨ Возможности  

- 📥 Получает от пользователя номер товара (только цифры).
- 🖼 Генерирует штрихкод **Code128** в **PNG**.
- 📄 Отправляет готовый файл обратно в чат.
- 🆘 Поддерживает кнопку **"Помощь"** с подсказками по вводу данных.
- 📝 Ведёт логирование в файл **logs/bot.log**.
- ✅ Тестируется через **pytest (Python)** и **JUnit5 (Java)**.
- 🔄 Автоматически деплоится в **Docker** через **Jenkins**. 

---

## 🎬 Пример работы  

<p align="center">
    <img src="images/demo1.jpg" alt="Пример работы бота" width="200"/>
    <img src="images/demo2.jpg" alt="Пример работы бота" width="200"/>
    <img src="images/demo3.jpg" alt="Пример работы бота" width="200"/>
</p>
 

---

## 🚀 Быстрый старт  

### 1. Получите токен бота  
Создайте нового бота через [BotFather](https://t.me/BotFather) и скопируйте выданный `BOT_TOKEN`.  

### 2. Загрузить готовый контейнер Docker

    docker pull kushogimi/testkodik_bot:v1.3

### 3. Запустите контейнер

    docker run -e BOT_TOKEN=ваш_токен kushogimi/testkodik_bot:v1.3
    
---

## ⚙️ Локальный запуск (без Docker)

Если хотите развернуть проект у себя локально:

    # Клонируем репозиторий
    git clone https://github.com/kushogimi/testkodik-bot.git
    cd testkodik-bot

    # Создаём виртуальное окружение
    python -m venv .venv
    source .venv/bin/activate   # Linux/Mac
    .venv\Scripts\activate      # Windows

    # Устанавливаем зависимости
    pip install -r requirements.txt

    # Добавляем BOT_TOKEN в .env
    echo "BOT_TOKEN=ваш_токен" > .env

    # Запускаем бота
    python bot.py

---

## 🧪 Тестирование

**Python (pytest)**
    
    pytest --maxfail=1 --disable-warnings -q

Файл тестов: *tests/test_barcode.py*

**Java (JUnit5)**

    cd java-tests
    mvn clean test

Файл тестов: *java-tests/src/test/java/BotApiTest.java*

---

## 🔄 CI/CD с Jenkins

Проект содержит Jenkinsfile, который выполняет:

1. 📥 Клонирование репозитория 
2. 🐍 Запуск **Python**-тестов (**pytest**)
3. ☕ Запуск **Java**-тестов (**JUnit5**)
4. 🐳 Сборку **Docker**-образа 
5. ☁️ Публикацию образа в **DockerHub** 
6. 🚀 Деплой контейнера с ботом

---

## 📂 Структура проекта

    testkodik-bot/
    ├─ logs/                # Директория для логов
    │  └─ bot.log
    ├─ tests/               # Python-тесты (pytest)
    │  └─ test_barcode.py
    ├─ java-tests/          # Java-тесты (JUnit)
    │  ├─ pom.xml
    │  └─ src/test/java/
    │     └─ BotApiTest.java
    ├─ bot.py               # Основной файл бота
    ├─ config.py            # Загрузка конфигурации (BOT_TOKEN)
    ├─ requirements.txt     # Зависимости Python
    ├─ Dockerfile           # Docker-сборка
    ├─ Jenkinsfile          # CI/CD-пайплайн
    ├─ .dockerignore
    ├─ .gitignore
    └─ README.md

---

## 🛠 Используемые библиотеки

- **python-telegram-bot** — работа с Telegram API
- **python-barcode** — генерация штрихкодов (EAN-13, Code128 и др.)
- **Pillow** — обработка изображени
- **python-dotenv** — работа с .env файлами
- **pytest** — тестирование Python-кода
- **JUnit5** — тестирование Java-кода
- **logging** — встроенное логирование Python
- **Docker** — упаковка приложения
- **Jenkins** — автоматизация CI/CD

