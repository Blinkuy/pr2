## 📦 Установка и запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/Blinkuy/pr2.git 
cd pr2
```

### 2. Создай виртуальное окружение

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

> 💡 Если файла `requirements.txt` нет, установи вручную:
> ```bash
> pip install fastapi uvicorn matplotlib jinja2 pillow
> ```

### 4. Запусти сервер разработки

```bash
uvicorn main:app --reload
```

### 5. Открой в браузере

🌐 [http://127.0.0.1:8000](http://127.0.0.1:8000) — веб-интерфейс  
📚 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Swagger API документация

---
