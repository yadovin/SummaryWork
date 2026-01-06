import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models import Operation
from storage import load_operations, save_operations
from utils import validate_date, validate_amount
from analysis import operations_to_df, plot_pie_by_category


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый планер")
        self.operations = load_operations()

        # --- Ввод операции ---
        tk.Label(root, text="Сумма").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Категория").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Комментарий").grid(row=3, column=0, padx=5, pady=5)
        self.comment_entry = tk.Entry(root)
        self.comment_entry.grid(row=3, column=1, padx=5, pady=5)

        self.type_var = tk.StringVar(value="expense")
        tk.Radiobutton(root, text="Расход", variable=self.type_var, value="expense").grid(row=4, column=0)
        tk.Radiobutton(root, text="Доход", variable=self.type_var, value="income").grid(row=4, column=1)

        tk.Button(root, text="Добавить операцию", command=self.add_operation).grid(row=5, column=0, columnspan=2,
                                                                                   pady=5)
        tk.Button(root, text="Анализ", command=self.analyze).grid(row=6, column=0, columnspan=2, pady=5)

        # --- Таблица для операций ---
        columns = ("date", "type", "category", "amount", "comment")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        self.tree.grid(row=0, column=2, rowspan=7, padx=10, pady=5)

        # Заголовки таблицы
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("category", text="Категория")
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("comment", text="Комментарий")

        # Размер колонок
        self.tree.column("date", width=90, anchor="center")
        self.tree.column("type", width=70, anchor="center")
        self.tree.column("category", width=100)
        self.tree.column("amount", width=80, anchor="center")
        self.tree.column("comment", width=150)

        self.update_tree()

    def add_operation(self):
        amount = self.amount_entry.get()
        date = self.date_entry.get()

        if not validate_amount(amount):
            messagebox.showerror("Ошибка", "Некорректная сумма")
            return

        if not validate_date(date):
            messagebox.showerror("Ошибка", "Некорректная дата")
            return

        try:
            op = Operation(
                float(amount),
                self.category_entry.get(),
                date,
                self.comment_entry.get(),
                self.type_var.get()
            )
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        self.operations.append(op)
        save_operations(self.operations)
        self.update_tree()
        messagebox.showinfo("Готово", "Операция добавлена")

    def update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for op in self.operations:
            self.tree.insert("", tk.END, values=(
                op.date.strftime("%Y-%m-%d"),
                op.op_type.upper(),
                op.category,
                f"{op.amount:.2f}",
                op.comment
            ))

    def analyze(self):
        df = operations_to_df(self.operations)

        # Круговая диаграмма расходов
        plot_pie_by_category(df, "expense")

        # Круговая диаграмма доходов
        plot_pie_by_category(df, "income")

