import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from PIL import Image, ImageTk
from datetime import datetime


class NeurobodrApp:
    def __init__(self, root):
        self.root = root
        self.root.title("НЕЙРОБОДР - Система мониторинга")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)


        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f'1000x650+{x}+{y}')


        self.colors = {
            'bg_dark': '#0A0F1F',
            'bg_medium': '#1A1F2F',
            'bg_light': '#2A2F3F',
            'accent_cyan': '#00FFF5',
            'accent_purple': '#9D4EDD',
            'accent_pink': '#FF006E',
            'text_primary': '#FFFFFF',
            'text_secondary': '#B0B0B0',
            'success': '#00FF9F',
            'warning': '#FFB800'
        }

        self.current_frame = None
        self.operator_data = {}
        self.reg_entries = {}
        self.photo_label = None
        self.content1 = None
        self.content2 = None
        self.content3 = None
        self.col1 = None
        self.col2 = None
        self.col3 = None
        self.photo_path = None

        self.setup_files()
        self.show_start_window()

    def setup_files(self):

        directories = ["data", "photos", "temp"]
        for dir_name in directories:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

        if not os.path.exists("data/operators.json"):
            with open("data/operators.json", "w", encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        if not os.path.exists("data/settings.json"):
            settings = {
                'last_operator': None,
                'theme': 'dark',
                'photo_quality': 95
            }
            with open("data/settings.json", "w", encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)

    def create_neon_button(self, parent, text, command, color, width=15, height=1):

        btn_frame = tk.Frame(parent, bg=self.colors['bg_medium'], highlightbackground=color,
                             highlightthickness=2, bd=0)

        btn = tk.Button(btn_frame, text=text, command=command,
                        font=('Orbitron', 10, 'bold'),
                        bg=self.colors['bg_medium'], fg=color,
                        width=width, height=height, bd=0, cursor='hand2',
                        activebackground=self.colors['bg_light'],
                        activeforeground=color)
        btn.pack(padx=3, pady=3)


        def on_enter(e):
            btn_frame.config(highlightbackground=color, highlightcolor=color)
            btn.config(fg='white')

        def on_leave(e):
            btn_frame.config(highlightbackground=color)
            btn.config(fg=color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn_frame

    def add_header(self, parent):

        header_frame = tk.Frame(parent, bg=self.colors['bg_dark'], height=120)
        header_frame.pack(fill=tk.X, pady=0)
        header_frame.pack_propagate(False)


        top_line = tk.Frame(header_frame, bg=self.colors['accent_cyan'], height=3)
        top_line.pack(fill=tk.X)


        content_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        content_frame.pack(expand=True, fill=tk.BOTH)


        title_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        title_frame.pack(expand=True)

        tk.Label(title_frame, text=" НЕЙРОБОДР ",
                 font=('Orbitron', 32, 'bold'),
                 bg=self.colors['bg_dark'],
                 fg=self.colors['accent_cyan']).pack()

        tk.Label(title_frame, text="система нейромониторинга водителей",
                 font=('Orbitron', 11),
                 bg=self.colors['bg_dark'],
                 fg=self.colors['text_secondary']).pack()


        bottom_line = tk.Frame(header_frame, bg=self.colors['accent_purple'], height=2)
        bottom_line.pack(fill=tk.X)

    def clear_window(self):

        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_start_window(self):

        self.clear_window()
        self.add_header(self.current_frame)


        main_container = tk.Frame(self.current_frame, bg=self.colors['bg_dark'])
        main_container.pack(expand=True, fill=tk.BOTH, padx=50, pady=30)


        grid_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        grid_frame.pack(expand=True)


        title_label = tk.Label(grid_frame,
                               text="ВЫБЕРИТЕ ДЕЙСТВИЕ",
                               font=('Orbitron', 18, 'bold'),
                               bg=self.colors['bg_dark'],
                               fg=self.colors['text_primary'])
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))


        btn_reg = self.create_neon_button(grid_frame, "РЕГИСТРАЦИЯ",
                                          self.show_registration_form,
                                          self.colors['accent_cyan'], width=20, height=2)
        btn_reg.grid(row=1, column=0, padx=20, pady=10)

        btn_auth = self.create_neon_button(grid_frame, "АВТОРИЗАЦИЯ",
                                           self.show_auth_form,
                                           self.colors['accent_purple'], width=20, height=2)
        btn_auth.grid(row=1, column=1, padx=20, pady=10)


        decor_frame = tk.Frame(grid_frame, bg=self.colors['bg_dark'])
        decor_frame.grid(row=2, column=0, columnspan=2, pady=40)


        status_frame = tk.Frame(decor_frame, bg=self.colors['bg_medium'],
                                relief=tk.FLAT, bd=0)
        status_frame.pack()

        tk.Label(status_frame, text="●", font=('Arial', 16),
                 bg=self.colors['bg_medium'], fg=self.colors['success']).pack(side=tk.LEFT, padx=10)

        tk.Label(status_frame, text="СИСТЕМА АКТИВНА",
                 font=('Orbitron', 10),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=10)


        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        time_label = tk.Label(main_container,
                              text=f"⏰ {current_time}",
                              font=('Orbitron', 10),
                              bg=self.colors['bg_dark'],
                              fg=self.colors['text_secondary'])
        time_label.pack(side=tk.BOTTOM, pady=10)


        def update_time():
            current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            time_label.config(text=f"⏰ {current_time}")
            self.root.after(1000, update_time)

        update_time()

    def show_registration_form(self):

        self.clear_window()
        self.add_header(self.current_frame)


        columns_container = tk.Frame(self.current_frame, bg=self.colors['bg_dark'])
        columns_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        self.col1 = self.create_modern_card(columns_container, "РЕГИСТРАЦИЯ",
                                            self.colors['accent_cyan'])
        self.col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.content1 = tk.Frame(self.col1, bg=self.colors['bg_medium'])
        self.content1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.show_registration_content()

        # Колонка 2 - Идентификация
        self.col2 = self.create_modern_card(columns_container, "ИДЕНТИФИКАЦИЯ",
                                            self.colors['accent_purple'])
        self.col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.content2 = tk.Frame(self.col2, bg=self.colors['bg_medium'])
        self.content2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.show_identification_content()


        self.col3 = self.create_modern_card(columns_container, "ИНФОРМАЦИЯ",
                                            self.colors['accent_pink'])
        self.col3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.content3 = tk.Frame(self.col3, bg=self.colors['bg_medium'])
        self.content3.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.show_info_content("Заполните форму регистрации")


        back_btn = self.create_neon_button(self.current_frame, "← НАЗАД",
                                           self.show_start_window,
                                           self.colors['text_secondary'], width=10, height=1)
        back_btn.pack(side=tk.BOTTOM, pady=10)

    def create_modern_card(self, parent, title, accent_color):
        """Создание стильной карточки"""
        card = tk.Frame(parent, bg=self.colors['bg_medium'],
                        highlightbackground=accent_color,
                        highlightthickness=2, bd=0)

        header = tk.Frame(card, bg=accent_color, height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text=title, font=('Orbitron', 12, 'bold'),
                 bg=accent_color, fg=self.colors['bg_dark']).pack(expand=True)

        return card

    def show_registration_content(self):

        fields = [
            ("ФАМИЛИЯ", "Пролыгин"),
            ("ИМЯ", "Максим"),
            ("ОТЧЕСТВО", "Алексеевич"),
            ("ВОЗРАСТ", "19"),
            ("ТЕЛЕФОН", "+7 (888) 888-88-88"),
            ("EMAIL", "example@mail.com")
        ]

        self.reg_entries = {}

        for label, default in fields:
            field_frame = tk.Frame(self.content1, bg=self.colors['bg_medium'])
            field_frame.pack(fill=tk.X, pady=5)

            tk.Label(field_frame, text=label, font=('Orbitron', 9),
                     bg=self.colors['bg_medium'],
                     fg=self.colors['text_secondary'],
                     anchor='w').pack(fill=tk.X)

            entry = tk.Entry(field_frame, font=('Consolas', 10),
                             bg=self.colors['bg_light'],
                             fg=self.colors['accent_cyan'],
                             insertbackground=self.colors['accent_cyan'],
                             bd=0, relief=tk.FLAT)
            entry.insert(0, default)
            entry.pack(fill=tk.X, pady=(2, 0), ipady=5)

            field_name = label.lower()
            self.reg_entries[field_name] = entry


        btn_save = self.create_neon_button(self.content1, "СОХРАНИТЬ",
                                           self.save_operator,
                                           self.colors['success'], width=15, height=1)
        btn_save.pack(pady=10)

        btn_clear = self.create_neon_button(self.content1, "ОЧИСТИТЬ",
                                            self.clear_form,
                                            self.colors['warning'], width=15, height=1)
        btn_clear.pack(pady=5)

    def clear_form(self):

        for entry in self.reg_entries.values():
            entry.delete(0, tk.END)

    def show_identification_content(self):


        photo_container = tk.Frame(self.content2, bg=self.colors['bg_light'],
                                   width=220, height=160,
                                   highlightbackground=self.colors['accent_purple'],
                                   highlightthickness=2)
        photo_container.pack(pady=10)
        photo_container.pack_propagate(False)

        self.photo_label = tk.Label(photo_container,
                                    bg=self.colors['bg_light'],
                                    text="📷\nФОТО НЕ ЗАГРУЖЕНО",
                                    fg=self.colors['text_secondary'],
                                    font=('Orbitron', 10))
        self.photo_label.pack(expand=True, fill=tk.BOTH)


        info_text = tk.Label(self.content2,
                             text="Требования: 600x600 px\nJPEG/PNG до 5MB",
                             font=('Orbitron', 8),
                             bg=self.colors['bg_medium'],
                             fg=self.colors['text_secondary'])
        info_text.pack(pady=5)


        upload_btn = self.create_neon_button(self.content2, "ЗАГРУЗИТЬ ФОТО",
                                             self.upload_photo,
                                             self.colors['accent_purple'], width=15, height=1)
        upload_btn.pack(pady=10)

    def show_info_content(self, text):

        info_frame = tk.Frame(self.content3, bg=self.colors['bg_medium'])
        info_frame.pack(fill=tk.BOTH, expand=True)


        tk.Label(info_frame, text="⚡", font=('Arial', 30),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['accent_cyan']).pack(pady=10)


        tk.Label(info_frame, text=text, font=('Orbitron', 10),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text_primary'],
                 wraplength=250).pack(pady=10)


        status_frame = tk.Frame(info_frame, bg=self.colors['bg_light'],
                                highlightbackground=self.colors['warning'],
                                highlightthickness=1)
        status_frame.pack(fill=tk.X, pady=10)

        tk.Label(status_frame, text="СТАТУС", font=('Orbitron', 9, 'bold'),
                 bg=self.colors['bg_light'],
                 fg=self.colors['warning']).pack(anchor='w', padx=10, pady=5)

        tk.Label(status_frame, text="Ожидание регистрации",
                 font=('Orbitron', 9),
                 bg=self.colors['bg_light'],
                 fg=self.colors['text_secondary']).pack(anchor='w', padx=10, pady=5)

    def save_operator(self):

        try:
            operator = {}
            for field_name, entry in self.reg_entries.items():
                value = entry.get().strip()
                if not value:
                    messagebox.showwarning("Предупреждение",
                                           f"Поле '{field_name}' не заполнено")
                    return
                operator[field_name] = value

            with open("data/operators.json", "r", encoding='utf-8') as f:
                operators = json.load(f)

            next_id = 1
            if operators:
                next_id = max(op.get('id', 0) for op in operators) + 1

            operator['id'] = next_id
            operator['registration_date'] = datetime.now().isoformat()
            operator['photo_path'] = self.photo_path

            operators.append(operator)

            with open("data/operators.json", "w", encoding='utf-8') as f:
                json.dump(operators, f, ensure_ascii=False, indent=4)

            self.operator_data = operator

            messagebox.showinfo("Успех", f"Оператор зарегистрирован с ID: {next_id}")


            tk.Label(self.content2, text=f"ID: {next_id}",
                     font=('Orbitron', 24, 'bold'),
                     bg=self.colors['bg_medium'],
                     fg=self.colors['accent_cyan']).pack(pady=5)

            self.update_info_block(f"Оператор {operator['фамилия']} {operator['имя']} зарегистрирован")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить оператора: {str(e)}")

    def update_info_block(self, message):

        if hasattr(self, 'content3'):
            for widget in self.content3.winfo_children():
                widget.destroy()

            info_frame = tk.Frame(self.content3, bg=self.colors['bg_medium'])
            info_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(info_frame, text="✓", font=('Arial', 40),
                     bg=self.colors['bg_medium'],
                     fg=self.colors['success']).pack(pady=10)

            tk.Label(info_frame, text=message, font=('Orbitron', 10),
                     bg=self.colors['bg_medium'],
                     fg=self.colors['text_primary'],
                     wraplength=250).pack(pady=10)

            success_frame = tk.Frame(info_frame, bg=self.colors['success'])
            success_frame.pack(fill=tk.X, pady=10)

            tk.Label(success_frame, text="ОПЕРАТОР ОПРЕДЕЛЕН",
                     font=('Orbitron', 11, 'bold'),
                     bg=self.colors['success'],
                     fg=self.colors['bg_dark']).pack(pady=5)

            tk.Label(success_frame, text=f"ID {self.operator_data.get('id', '')}",
                     font=('Orbitron', 10),
                     bg=self.colors['success'],
                     fg=self.colors['bg_dark']).pack(pady=5)

            next_btn = self.create_neon_button(info_frame, "ДАЛЕЕ →",
                                               self.next_step,
                                               self.colors['accent_cyan'], width=12, height=1)
            next_btn.pack(pady=10)

    def upload_photo(self):

        try:
            file_path = filedialog.askopenfilename(
                title="Выберите фото",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
            )

            if file_path:
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                if file_size > 5:
                    messagebox.showwarning("Предупреждение",
                                           "Файл слишком большой. Максимальный размер 5 MB")
                    return

                img = Image.open(file_path)
                img.thumbnail((220, 160), Image.Resampling.LANCZOS)

                if hasattr(self, 'operator_data') and self.operator_data.get('id'):
                    filename = f"operator_{self.operator_data['id']}.jpg"
                    save_path = os.path.join("photos", filename)
                    img.save(save_path, "JPEG", quality=95)
                    self.photo_path = save_path
                else:
                    temp_path = os.path.join("temp", "temp_photo.jpg")
                    img.save(temp_path, "JPEG", quality=95)
                    self.photo_path = temp_path

                photo = ImageTk.PhotoImage(img)
                if hasattr(self, 'photo_label') and self.photo_label:
                    self.photo_label.config(image=photo, text="")
                    self.photo_label.image = photo

                messagebox.showinfo("Успех", "Фото загружено успешно")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить фото: {str(e)}")

    def next_step(self):

        if messagebox.askyesno("Подтверждение",
                               "Завершить регистрацию и вернуться в главное меню?"):
            self.show_start_window()

    def show_auth_form(self):

        self.clear_window()
        self.add_header(self.current_frame)

        auth_card = self.create_modern_card(self.current_frame, "АВТОРИЗАЦИЯ",
                                            self.colors['accent_purple'])
        auth_card.pack(expand=True, padx=100, pady=50, fill=tk.BOTH)

        content = tk.Frame(auth_card, bg=self.colors['bg_medium'], padx=30, pady=30)
        content.pack(fill=tk.BOTH, expand=True)

        tk.Label(content, text="ВВЕДИТЕ ID ОПЕРАТОРА:",
                 font=('Orbitron', 11),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 10))

        id_entry = tk.Entry(content, font=('Consolas', 14),
                            bg=self.colors['bg_light'],
                            fg=self.colors['accent_cyan'],
                            insertbackground=self.colors['accent_cyan'],
                            bd=0, relief=tk.FLAT)
        id_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)


        try:
            with open("data/operators.json", "r", encoding='utf-8') as f:
                operators = json.load(f)

            if operators:
                tk.Label(content, text="ИЛИ ВЫБЕРИТЕ ИЗ СПИСКА:",
                         font=('Orbitron', 9),
                         bg=self.colors['bg_medium'],
                         fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))

                listbox = tk.Listbox(content, height=4,
                                     font=('Consolas', 10),
                                     bg=self.colors['bg_light'],
                                     fg=self.colors['text_primary'],
                                     selectbackground=self.colors['accent_purple'],
                                     selectforeground='white',
                                     bd=0, relief=tk.FLAT)
                listbox.pack(fill=tk.X, pady=(0, 10))

                for op in operators[-5:]:
                    listbox.insert(tk.END,
                                   f"ID {op['id']}: {op.get('фамилия', '')} {op.get('имя', '')}")

                def on_select(event):
                    selection = listbox.curselection()
                    if selection:
                        op = operators[selection[0]]
                        id_entry.delete(0, tk.END)
                        id_entry.insert(0, str(op['id']))

                listbox.bind('<<ListboxSelect>>', on_select)

        except Exception as e:
            pass


        button_frame = tk.Frame(content, bg=self.colors['bg_medium'])
        button_frame.pack(fill=tk.X, pady=20)

        login_btn = self.create_neon_button(button_frame, "ВОЙТИ",
                                            lambda: self.check_auth(id_entry.get()),
                                            self.colors['accent_purple'], width=10, height=1)
        login_btn.pack(side=tk.LEFT, padx=5)

        back_btn = self.create_neon_button(button_frame, "НАЗАД",
                                           self.show_start_window,
                                           self.colors['text_secondary'], width=10, height=1)
        back_btn.pack(side=tk.LEFT, padx=5)

    def check_auth(self, id_str):

        try:
            if not id_str.strip():
                messagebox.showwarning("Предупреждение", "Введите ID оператора")
                return

            operator_id = int(id_str)

            with open("data/operators.json", "r", encoding='utf-8') as f:
                operators = json.load(f)

            for op in operators:
                if op.get('id') == operator_id:
                    self.operator_data = op
                    messagebox.showinfo("Успех",
                                        f"Добро пожаловать, {op.get('фамилия', '')} {op.get('имя', '')}!")
                    self.show_authorized_view()
                    return

            messagebox.showerror("Ошибка", f"Оператор с ID {operator_id} не найден")

        except ValueError:
            messagebox.showerror("Ошибка", "ID должен быть числом")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка авторизации: {str(e)}")

    def show_authorized_view(self):

        self.clear_window()
        self.add_header(self.current_frame)

        columns_container = tk.Frame(self.current_frame, bg=self.colors['bg_dark'])
        columns_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        col1 = self.create_modern_card(columns_container, "ДАННЫЕ ОПЕРАТОРА",
                                       self.colors['accent_cyan'])
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        content1 = tk.Frame(col1, bg=self.colors['bg_medium'])
        content1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for key, value in self.operator_data.items():
            if key not in ['id', 'registration_date', 'photo_path']:
                frame = tk.Frame(content1, bg=self.colors['bg_light'])
                frame.pack(fill=tk.X, pady=2)

                tk.Label(frame, text=f"{key.upper()}:",
                         font=('Orbitron', 9, 'bold'),
                         bg=self.colors['bg_light'],
                         fg=self.colors['accent_cyan'],
                         width=12, anchor='w').pack(side=tk.LEFT, padx=5, pady=5)

                tk.Label(frame, text=str(value),
                         font=('Consolas', 9),
                         bg=self.colors['bg_light'],
                         fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=5, pady=5)


        col2 = self.create_modern_card(columns_container, "ИДЕНТИФИКАЦИЯ",
                                       self.colors['accent_purple'])
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        content2 = tk.Frame(col2, bg=self.colors['bg_medium'])
        content2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(content2, text=f"ID {self.operator_data.get('id', '')}",
                 font=('Orbitron', 24, 'bold'),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['accent_purple']).pack(pady=10)


        if self.operator_data.get('photo_path') and os.path.exists(self.operator_data['photo_path']):
            try:
                img = Image.open(self.operator_data['photo_path'])
                img.thumbnail((220, 160))
                photo = ImageTk.PhotoImage(img)

                photo_label = tk.Label(content2, image=photo, bg=self.colors['bg_medium'])
                photo_label.image = photo
                photo_label.pack(pady=10)
            except:
                tk.Label(content2, text="Фото не найдено",
                         font=('Orbitron', 10),
                         bg=self.colors['bg_medium'],
                         fg=self.colors['text_secondary']).pack(pady=10)
        else:
            tk.Label(content2, text="📷\nФОТО ОТСУТСТВУЕТ",
                     font=('Orbitron', 10),
                     bg=self.colors['bg_medium'],
                     fg=self.colors['text_secondary']).pack(pady=10)


        col3 = self.create_modern_card(columns_container, "СТАТУС",
                                       self.colors['success'])
        col3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        content3 = tk.Frame(col3, bg=self.colors['bg_medium'])
        content3.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        status_frame = tk.Frame(content3, bg=self.colors['success'])
        status_frame.pack(fill=tk.X, pady=10)

        tk.Label(status_frame, text="АВТОРИЗОВАН",
                 font=('Orbitron', 12, 'bold'),
                 bg=self.colors['success'],
                 fg=self.colors['bg_dark']).pack(pady=5)

        current_time = datetime.now().strftime("%H:%M:%S")
        tk.Label(content3, text=f"⏰ {current_time}",
                 font=('Orbitron', 10),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text_secondary']).pack(pady=5)

        tk.Label(content3, text=datetime.now().strftime("%d.%m.%Y"),
                 font=('Orbitron', 10),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text_secondary']).pack(pady=5)

        monitor_btn = self.create_neon_button(content3, "ЗАПУСК МОНИТОРИНГА",
                                              self.start_monitoring,
                                              self.colors['accent_cyan'], width=15, height=1)
        monitor_btn.pack(pady=10)

        exit_btn = self.create_neon_button(content3, "ВЫХОД",
                                           self.show_start_window,
                                           self.colors['accent_pink'], width=15, height=1)
        exit_btn.pack(pady=5)

    def start_monitoring(self):

        messagebox.showinfo("Мониторинг",
                            "⚡ СИСТЕМА МОНИТОРИНГА АКТИВИРОВАНА ⚡\n\n"
                            "Отслеживание состояния водителя начато...\n"
                            "(демо-режим)")


if __name__ == "__main__":
    root = tk.Tk()
    app = NeurobodrApp(root)
    root.mainloop()