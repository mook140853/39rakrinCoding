import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "homework_tasks.json"


# =========================
# โหลด / บันทึกข้อมูล
# =========================

def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass

    return [
        {
            "title": "ทำการบ้านคณิตศาสตร์",
            "subject": "คณิตศาสตร์",
            "due": "18/08/2026 18:00",
            "priority": "สูง",
            "done": False
        },
        {
            "title": "อ่านหนังสือวิทยาศาสตร์",
            "subject": "วิทยาศาสตร์",
            "due": "19/08/2026 20:00",
            "priority": "กลาง",
            "done": False
        }
    ]


def save_tasks():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


tasks = load_tasks()


# =========================
# สี
# =========================

BLUE = "#1677FF"
LIGHT_BLUE = "#EAF3FF"
BACKGROUND = "#F4F8FF"
WHITE = "#FFFFFF"
TEXT = "#17233D"
GRAY = "#71809A"
GREEN = "#18A873"
RED = "#E85252"
ORANGE = "#F39C32"


# =========================
# หน้าต่างหลัก
# =========================

root = tk.Tk()
root.title("Homework Buddy")
root.geometry("1100x700")
root.minsize(850, 600)
root.configure(bg=BACKGROUND)


# =========================
# ฟังก์ชัน
# =========================

def update_dashboard():
    for widget in task_frame.winfo_children():
        widget.destroy()

    total = len(tasks)
    completed = sum(1 for task in tasks if task["done"])
    pending = total - completed

    total_label.config(text=str(total))
    completed_label.config(text=str(completed))
    pending_label.config(text=str(pending))

    if total > 0:
        percent = int(completed / total * 100)
    else:
        percent = 0

    progress["value"] = percent
    percent_label.config(text=f"{percent}%")

    summary_label.config(
        text=f"วันนี้มีงานค้าง {pending} งาน"
        if pending
        else "วันนี้ไม่มีงานค้างแล้ว 🎉"
    )

    if current_filter.get() == "todo":
        show = [t for t in tasks if not t["done"]]
    else:
        show = [t for t in tasks if t["done"]]

    if not show:
        empty = tk.Label(
            task_frame,
            text="ยังไม่มีงานในรายการนี้ 🎉",
            bg=WHITE,
            fg=GRAY,
            font=("Tahoma", 14),
            pady=40
        )
        empty.pack(fill="x")
        return

    for index, task in enumerate(show):
        create_task_card(task, index)


def create_task_card(task, index):

    card = tk.Frame(
        task_frame,
        bg=WHITE,
        highlightbackground="#E2E9F2",
        highlightthickness=1
    )

    card.pack(
        fill="x",
        pady=6,
        padx=5
    )

    # ปุ่มเสร็จ
    check_button = tk.Button(
        card,
        text="✓" if task["done"] else "○",
        font=("Arial", 18, "bold"),
        bg="#EAF3FF" if not task["done"] else "#E5F7EF",
        fg=BLUE if not task["done"] else GREEN,
        bd=0,
        width=3,
        cursor="hand2",
        command=lambda t=task: toggle_task(t)
    )

    check_button.pack(
        side="left",
        padx=12,
        pady=12
    )

    # ส่วนข้อมูล
    info = tk.Frame(
        card,
        bg=WHITE
    )

    info.pack(
        side="left",
        fill="both",
        expand=True,
        pady=10
    )

    title = tk.Label(
        info,
        text=task["title"],
        bg=WHITE,
        fg=TEXT,
        font=("Tahoma", 13, "bold"),
        anchor="w"
    )

    title.pack(
        anchor="w"
    )

    detail = tk.Label(
        info,
        text=f'{task["subject"]}   •   ส่ง {task["due"]}',
        bg=WHITE,
        fg=GRAY,
        font=("Tahoma", 10),
        anchor="w"
    )

    detail.pack(
        anchor="w",
        pady=(4, 0)
    )

    # ความสำคัญ
    priority_color = {
        "สูง": RED,
        "กลาง": ORANGE,
        "ต่ำ": GREEN
    }

    priority = tk.Label(
        card,
        text=task["priority"],
        bg=priority_color.get(
            task["priority"],
            GRAY
        ),
        fg=WHITE,
        font=("Tahoma", 9, "bold"),
        padx=10,
        pady=5
    )

    priority.pack(
        side="right",
        padx=8
    )

    # ปุ่มลบ
    delete_button = tk.Button(
        card,
        text="ลบ",
        bg="#F1F4F8",
        fg=TEXT,
        bd=0,
        padx=10,
        pady=6,
        cursor="hand2",
        command=lambda t=task: delete_task(t)
    )

    delete_button.pack(
        side="right",
        padx=5
    )


def toggle_task(task):
    task["done"] = not task["done"]
    save_tasks()
    update_dashboard()


def delete_task(task):

    answer = messagebox.askyesno(
        "ลบงาน",
        f'ต้องการลบ "{task["title"]}" หรือไม่?'
    )

    if answer:
        tasks.remove(task)
        save_tasks()
        update_dashboard()


def add_task():

    title = title_entry.get().strip()
    subject = subject_entry.get().strip()
    due = due_entry.get().strip()
    priority = priority_combo.get()

    if not title:
        messagebox.showwarning(
            "ข้อมูลไม่ครบ",
            "กรุณาใส่ชื่องาน"
        )
        return

    if not subject:
        subject = "ทั่วไป"

    if not due:
        due = "ยังไม่ได้กำหนด"

    new_task = {
        "title": title,
        "subject": subject,
        "due": due,
        "priority": priority,
        "done": False
    }

    tasks.insert(0, new_task)

    save_tasks()

    title_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)

    update_dashboard()

    messagebox.showinfo(
        "สำเร็จ",
        "เพิ่มงานเรียบร้อยแล้ว ✅"
    )


def show_todo():
    current_filter.set("todo")

    todo_button.config(
        bg=BLUE,
        fg=WHITE
    )

    done_button.config(
        bg="#EDF3FA",
        fg=TEXT
    )

    update_dashboard()


def show_done():
    current_filter.set("done")

    done_button.config(
        bg=BLUE,
        fg=WHITE
    )

    todo_button.config(
        bg="#EDF3FA",
        fg=TEXT
    )

    update_dashboard()


def clear_completed():

    completed_tasks = [
        task for task in tasks
        if task["done"]
    ]

    if not completed_tasks:
        messagebox.showinfo(
            "ไม่มีงาน",
            "ยังไม่มีงานที่เสร็จแล้ว"
        )
        return

    answer = messagebox.askyesno(
        "ล้างงาน",
        f"ต้องการลบงานที่เสร็จแล้ว {len(completed_tasks)} งานหรือไม่?"
    )

    if answer:

        tasks[:] = [
            task for task in tasks
            if not task["done"]
        ]

        save_tasks()
        update_dashboard()


# =========================
# Header
# =========================

header = tk.Frame(
    root,
    bg=BLUE,
    height=180
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


header_content = tk.Frame(
    header,
    bg=BLUE
)

header_content.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=20
)


logo = tk.Label(
    header_content,
    text="✓ Homework Buddy",
    bg=BLUE,
    fg=WHITE,
    font=("Tahoma", 20, "bold")
)

logo.pack(
    anchor="w"
)


title_header = tk.Label(
    header_content,
    text="สวัสดีครับ! 👋",
    bg=BLUE,
    fg=WHITE,
    font=("Tahoma", 25, "bold")
)

title_header.pack(
    anchor="w",
    pady=(15, 2)
)


summary_label = tk.Label(
    header_content,
    text="",
    bg=BLUE,
    fg=WHITE,
    font=("Tahoma", 11)
)

summary_label.pack(
    anchor="w"
)


# =========================
# เนื้อหาหลัก
# =========================

main = tk.Frame(
    root,
    bg=BACKGROUND
)

main.pack(
    fill="both",
    expand=True
)


# =========================
# ซ้าย
# =========================

left = tk.Frame(
    main,
    bg=BACKGROUND
)

left.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(25, 10),
    pady=20
)


task_header = tk.Frame(
    left,
    bg=WHITE
)

task_header.pack(
    fill="x"
)


task_title = tk.Label(
    task_header,
    text="Priority Tasks",
    bg=WHITE,
    fg=TEXT,
    font=("Tahoma", 17, "bold")
)

task_title.pack(
    side="left",
    padx=18,
    pady=15
)


current_filter = tk.StringVar(
    value="todo"
)


todo_button = tk.Button(
    task_header,
    text="ต้องทำ",
    bg=BLUE,
    fg=WHITE,
    bd=0,
    padx=12,
    pady=7,
    cursor="hand2",
    command=show_todo
)

todo_button.pack(
    side="right",
    padx=5
)


done_button = tk.Button(
    task_header,
    text="เสร็จแล้ว",
    bg="#EDF3FA",
    fg=TEXT,
    bd=0,
    padx=12,
    pady=7,
    cursor="hand2",
    command=show_done
)

done_button.pack(
    side="right",
    padx=5
)


# =========================
# รายการงาน
# =========================

task_canvas = tk.Canvas(
    left,
    bg=WHITE,
    highlightthickness=0
)

task_scroll = ttk.Scrollbar(
    left,
    orient="vertical",
    command=task_canvas.yview
)

task_canvas.configure(
    yscrollcommand=task_scroll.set
)


task_scroll.pack(
    side="right",
    fill="y"
)

task_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


task_frame = tk.Frame(
    task_canvas,
    bg=WHITE
)


canvas_window = task_canvas.create_window(
    (0, 0),
    window=task_frame,
    anchor="nw"
)


def resize_task_frame(event):
    task_canvas.itemconfig(
        canvas_window,
        width=event.width
    )


task_canvas.bind(
    "<Configure>",
    resize_task_frame
)


def update_scroll(event=None):
    task_canvas.configure(
        scrollregion=task_canvas.bbox("all")
    )


task_frame.bind(
    "<Configure>",
    update_scroll
)


# =========================
# ขวา
# =========================

right = tk.Frame(
    main,
    bg=BACKGROUND,
    width=300
)

right.pack(
    side="right",
    fill="y",
    padx=(10, 25),
    pady=20
)


# =========================
# สถิติ
# =========================

stats_card = tk.Frame(
    right,
    bg=WHITE
)

stats_card.pack(
    fill="x"
)


stats_title = tk.Label(
    stats_card,
    text="📊 ภาพรวม",
    bg=WHITE,
    fg=TEXT,
    font=("Tahoma", 17, "bold")
)

stats_title.pack(
    anchor="w",
    padx=18,
    pady=15
)


stats_frame = tk.Frame(
    stats_card,
    bg=WHITE
)

stats_frame.pack(
    fill="x",
    padx=12
)


pending_box = tk.Frame(
    stats_frame,
    bg="#F5F9FF"
)

pending_box.pack(
    side="left",
    fill="both",
    expand=True,
    padx=4,
    pady=5
)


tk.Label(
    pending_box,
    text="ค้างอยู่",
    bg="#F5F9FF",
    fg=GRAY,
    font=("Tahoma", 10)
).pack(
    pady=(10, 0)
)


pending_label = tk.Label(
    pending_box,
    text="0",
    bg="#F5F9FF",
    fg=TEXT,
    font=("Tahoma", 25, "bold")
)

pending_label.pack(
    pady=(2, 10)
)


completed_box = tk.Frame(
    stats_frame,
    bg="#F5F9FF"
)

completed_box.pack(
    side="left",
    fill="both",
    expand=True,
    padx=4,
    pady=5
)


tk.Label(
    completed_box,
    text="เสร็จแล้ว",
    bg="#F5F9FF",
    fg=GRAY,
    font=("Tahoma", 10)
).pack(
    pady=(10, 0)
)


completed_label = tk.Label(
    completed_box,
    text="0",
    bg="#F5F9FF",
    fg=TEXT,
    font=("Tahoma", 25, "bold")
)

completed_label.pack(
    pady=(2, 10)
)


tk.Label(
    stats_card,
    text="ความคืบหน้า",
    bg=WHITE,
    fg=GRAY,
    font=("Tahoma", 10)
).pack(
    anchor="w",
    padx=18,
    pady=(15, 5)
)


progress = ttk.Progressbar(
    stats_card,
    orient="horizontal",
    mode="determinate",
    maximum=100
)

progress.pack(
    fill="x",
    padx=18
)


percent_label = tk.Label(
    stats_card,
    text="0%",
    bg=WHITE,
    fg=GRAY,
    font=("Tahoma", 10)
)

percent_label.pack(
    anchor="w",
    padx=18,
    pady=8
)


total_label = tk.Label(
    header_content,
    text="0",
    bg=BLUE,
    fg=BLUE
)

completed_label
# =========================
# เพิ่มงาน
# =========================

add_card = tk.Frame(
    right,
    bg=WHITE
)

add_card.pack(
    fill="x",
    pady=20
)


tk.Label(
    add_card,
    text="➕ เพิ่มงานใหม่",
    bg=WHITE,
    fg=TEXT,
    font=("Tahoma", 17, "bold")
).pack(
    anchor="w",
    padx=18,
    pady=15
)


tk.Label(
    add_card,
    text="ชื่องาน",
    bg=WHITE,
    fg=TEXT,
    font=("Tahoma", 10, "bold")
).pack(
    anchor="w",
    padx=18
)


title_entry = tk.Entry(
    add_card,
    font=("Tahoma", 10)
)

title_entry.pack(
    fill="x",
    padx=18,
    pady=5
)


tk.Label(
    add_card,
    text="วิชา",
    bg=WHITE,
    fg=TEXT,
    font=("Tahoma", 10, "bold")
).pack(
    anchor="w",
    padx=18,
    pady=(5, 0)
)


subject_entry = tk.Entry(
    add_card,
    font=("Tahoma", 10)
)

subject_entry.pack(
    fill="x",
    padx=18,
    pady=5
)


tk.Label(
    add_card,
    text="กำหนดส่ง",
    bg=WHITE,
    fg=TEXT,
    font=("Tahoma", 10, "bold")
).pack(
    anchor="w",
    padx=18,
    pady=(5, 0)
)


due_entry = tk.Entry(
    add_card,
    font=("Tahoma", 10)
)

due_entry.insert(
    0,
    "18/08/2026 18:00"
)

due_entry.pack(
    fill="x",
    padx=18,
    pady=5
)


tk.Label(
    add_card,
    text="ความสำคัญ",
    bg=WHITE,
    fg=TEXT,
    font=("Tahoma", 10, "bold")
).pack(
    anchor="w",
    padx=18,
    pady=(5, 0)
)


priority_combo = ttk.Combobox(
    add_card,
    values=[
        "สูง",
        "กลาง",
        "ต่ำ"
    ],
    state="readonly"
)

priority_combo.set("กลาง")

priority_combo.pack(
    fill="x",
    padx=18,
    pady=5
)


add_button = tk.Button(
    add_card,
    text="บันทึกงาน",
    bg=BLUE,
    fg=WHITE,
    bd=0,
    padx=15,
    pady=10,
    cursor="hand2",
    command=add_task
)

add_button.pack(
    fill="x",
    padx=18,
    pady=15
)


# =========================
# ปุ่มล้างงาน
# =========================

clear_button = tk.Button(
    right,
    text="🧹 ล้างงานที่เสร็จแล้ว",
    bg="#EDF4FF",
    fg=BLUE,
    bd=0,
    padx=10,
    pady=10,
    cursor="hand2",
    command=clear_completed
)

clear_button.pack(
    fill="x"
)


# =========================
# เริ่มโปรแกรม
# =========================

update_dashboard()

root.mainloop()