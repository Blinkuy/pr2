from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import io
import base64


def lagrange_interp(x: float, points: List[Tuple[float, float]]) -> float:
    """Метод Лагранжа для любого количества точек"""
    n = len(points)
    result = 0.0
    for i in range(n):
        xi, yi = points[i]
        term = yi
        for j in range(n):
            if i != j:
                xj, _ = points[j]
                term *= (x - xj) / (xi - xj)
        result += term
    return result


def plot_to_base64(points: List[Tuple[float, float]],
                   result_point: Tuple[float, float],
                   title: str) -> str:
    plt.figure(figsize=(8, 5))

    px, py = zip(*points)
    plt.plot(px, py, 'ro', label='Исходные точки', markersize=8)
    plt.plot(result_point[0], result_point[1], 'b*',
             label='Результат', markersize=15)

    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return base64.b64encode(buf.getvalue()).decode('utf-8')


app = FastAPI(title="Интерполяция Лагранжа")

templates = Jinja2Templates(directory="templates")

PRESETS = [
    {"name": "Задача 1", "points": [(6, -12), (14, 6), (16, 8)], "x": 12},
    {"name": "Задача 2", "points": [(2, -5), (14, -0.5)], "x": 10},
    {"name": "Задача 3", "points": [(12, -4), (18, 6)], "x": 15},
    {"name": "Задача 4", "points": [(6, 2), (14, 6), (15, 8)], "x": 9},
    {"name": "Задача 5", "points": [(-10, -7.2), (-4, -5), (16, -2)], "x": 14},
]



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница с формой"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "task_name": "Задача 1",
        "points": "",
        "target_x": 12
    })


@app.post("/solve", response_class=HTMLResponse)
async def solve_task(
        request: Request,
        task_name: str = Form(...),
        points: str = Form(...),
        target_x: float = Form(...)
):
    try:
        points_list = []
        for line in points.strip().split('\n'):
            line = line.strip()
            if line:
                x, y = map(float, line.split(','))
                points_list.append((x, y))

        if len(points_list) < 2:
            raise ValueError("Нужно минимум 2 точки!")

        y = lagrange_interp(target_x, points_list)

        img_base64 = plot_to_base64(points_list, (target_x, y), task_name)

        return templates.TemplateResponse("result.html", {
            "request": request,
            "task_name": task_name,
            "points": points_list,
            "target_x": target_x,
            "calculated_y": f"{y:.4f}",
            "image_base64": img_base64
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "task_name": task_name,
            "points": points,
            "target_x": target_x,
            "error": str(e)
        })


@app.get("/solve_all", response_class=HTMLResponse)
async def solve_all(request: Request):
    """Решить все 5 задач сразу"""
    tasks_data = []

    for task in PRESETS:
        y = lagrange_interp(task["x"], task["points"])
        img = plot_to_base64(task["points"], (task["x"], y), task["name"])

        tasks_data.append({
            "name": task["name"],
            "x": task["x"],
            "y": f"{y:.4f}",
            "image_base64": img
        })

    return templates.TemplateResponse("solve_all.html", {
        "request": request,
        "tasks": tasks_data
    })


@app.get("/task6", response_class=HTMLResponse)
async def task6(request: Request):
    """Задача 6 - все точки на одном графике"""
    # Считаем все найденные точки
    found_points = []
    results_table = []

    for i, task in enumerate(PRESETS, 1):
        y = lagrange_interp(task["x"], task["points"])
        found_points.append((task["x"], y))
        results_table.append({
            "num": i,
            "name": task["name"],
            "x": task["x"],
            "y": f"{y:.4f}"
        })

    # Строим общий график
    plt.figure(figsize=(12, 7))
    x_vals, y_vals = zip(*found_points)
    plt.plot(x_vals, y_vals, 'bo-', label='Найденные точки',
             markersize=12, linewidth=2)

    # Подписываем точки
    for i, (x, y) in enumerate(found_points, 1):
        plt.annotate(f'{i} ({x}, {y:.1f})', (x, y), textcoords="offset points",
                     xytext=(5, 5), ha='left', fontsize=10, fontweight='bold')

    plt.title('Задача 6: Все найденные точки (Вариант 2)', fontsize=14)
    plt.grid(True, alpha=0.4)
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.legend()
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return templates.TemplateResponse("task6.html", {
        "request": request,
        "image_base64": img_base64,
        "results": results_table
    })
