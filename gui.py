import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from models import Operation
from storage import load_operations, save_operations
from utils import validate_date, validate_amount
from analysis import operations_to_df, plot_pie_by_category, plot_monthly_summary


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый планер")
        self.operations = load_operations()


        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)


        input_frame = tk.LabelFrame(left_frame, text="Добавить операцию")
        input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)


        tk.Label(input_frame, text="Сумма").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(input_frame, text="Категория").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.category_entry = tk.Entry(input_frame)
        self.category_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(input_frame, text="Дата (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(input_frame, text="Комментарий").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.comment_entry = tk.Entry(input_frame)
        self.comment_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)


        type_frame = tk.Frame(input_frame)
        type_frame.grid(row=4, column=0, columnspan=2, pady=5)
        self.type_var = tk.StringVar(value="expense")
        tk.Radiobutton(type_frame, text="Расход", variable=self.type_var, value="expense").pack(side="left")
        tk.Radiobutton(type_frame, text="Доход", variable=self.type_var, value="income").pack(side="left")


        tk.Button(input_frame, text="Добавить операцию", command=self.add_operation).grid(row=5, column=0, columnspan=1,
                                                                                          pady=5, sticky="ew")

        tk.Button(input_frame, text="Удалить операцию", command=self.delete_selected_operation).grid(row=5, column=1, columnspan=1,
                                                                                          pady=5, sticky="ew")



        filter_frame = tk.LabelFrame(left_frame, text="Фильтр по дате")
        filter_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)

        tk.Label(filter_frame, text="Дата с").grid(row=0, column=0, padx=5, pady=2)
        self.start_date_entry = tk.Entry(filter_frame, width=12)
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(filter_frame, text="по").grid(row=0, column=2, padx=5, pady=2)
        self.end_date_entry = tk.Entry(filter_frame, width=12)
        self.end_date_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5,
                                                                                         pady=2)
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filter).grid(row=0, column=5, padx=5, pady=2)


        actions_frame = tk.Frame(left_frame)
        actions_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=10)

        tk.Button(actions_frame, text="Анализ", command=self.analyze).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(actions_frame, text="График по месяцам", command=self.show_monthly_chart).pack(side="left",
                                                                                                 expand=True, fill="x",
                                                                                                 padx=5)
        columns = ("date", "type", "category", "amount", "comment")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
        self.tree.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)


        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("category", text="Категория")
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("comment", text="Комментарий")

        self.tree.column("date", width=90, anchor="center")
        self.tree.column("type", width=70, anchor="center")
        self.tree.column("category", width=100)
        self.tree.column("amount", width=80, anchor="center")
        self.tree.column("comment", width=150)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

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
        save_operations([op])
        self.update_tree()
        messagebox.showinfo("Готово", "Операция добавлена")

    def update_tree(self, df=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if df is None:
            df = operations_to_df(self.operations)
        for _, op in df.iterrows():
            self.tree.insert("", tk.END, values=(
                op["date"].strftime("%Y-%m-%d") if isinstance(op["date"], pd.Timestamp) else op["date"],
                op["op_type"].capitalize(),
                op["category"],
                f"{float(op['amount']):.2f}",
                op["comment"]
            ))

    def analyze(self):
        df = self.get_filtered_data()
        plot_pie_by_category(df, "expense")
        plot_pie_by_category(df, "income")

    def apply_filter(self):
        df = operations_to_df(self.operations)
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        if validate_date(start_date_str) and validate_date(end_date_str):
            start_date = pd.to_datetime(start_date_str)
            end_date = pd.to_datetime(end_date_str)
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        self.update_tree(df)


    def reset_filter(self):
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.update_tree()


    def get_filtered_data(self):
        df = operations_to_df(self.operations)
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()
        if validate_date(start_date_str) and validate_date(end_date_str):
            start_date = pd.to_datetime(start_date_str)
            end_date = pd.to_datetime(end_date_str)
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        return df


    def show_monthly_chart(self):
        df = operations_to_df(self.operations)
        if df.empty:
            messagebox.showinfo("Информация", "Нет данных для построения графика")
            return

        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        if validate_date(start_date_str) and validate_date(end_date_str):
            start_date = pd.to_datetime(start_date_str)
            end_date = pd.to_datetime(end_date_str)
            plot_monthly_summary(df, start_date, end_date)
        else:
            plot_monthly_summary(df)

    def delete_selected_operation(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Удаление", "Выберите строку для удаления")
            return

        values = self.tree.item(selected_item, 'values')
        date_str, op_type, category, amount_str, comment = values

        date_obj = pd.to_datetime(date_str)

        self.operations = [
            op for op in self.operations
            if not (
                    op.date == date_obj and
                    op.op_type == op_type.lower() and
                    op.category == category and
                    f"{op.amount:.2f}" == amount_str and
                    op.comment == comment
            )
        ]

        save_operations(self.operations, overwrite=True)

        self.update_tree()

        messagebox.showinfo("Удаление", "Запись удалена")