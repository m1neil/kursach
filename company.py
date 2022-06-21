from random import randint
from window import Window
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from child_window import Child_window
from client import Client
from close_window import Close_window
import sqlite3
import hashlib


class Company:
    def __init__(self) -> None:
        self.name = "Creditime"
        self.window = Window(self.name, 500, 500, 800, 250, "icon/creditime.ico", (True, True))
        self.close_win = Close_window(self.window)
        self.database = sqlite3.connect("databases/clients.db")
        self.cursor = self.database.cursor()
        self.user = Client()
        query = """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(30),
            last_name VARCHAR(30),
            email VARCHAR,
            password VARCHAR,
            phone VARCHAR(13),
            age INT,
            work_place VARCHAR,
            work_position VARCHAR,
            salary FLOAT NOT NULL DEFAULT 0,
            credit FLOAT NOT NULL DEFAULT 0,
            sum_use_credit FLOAT NOT NULL DEFAULT 0,
            credit_days VARCHAR NOT NULL DEFAULT 0,
            regular_client INT NOT NULL DEFAULT 0
            )"""
        self.database.execute(query)
        self.database.commit()
        self.cursor.close()
        self.database.close()
        self.card_database = sqlite3.connect("databases/cards.db")
        self.card_cursor = self.card_database.cursor()
        card_query = """CREATE TABLE IF NOT EXISTS users_cards (
            number_card INT,
            balanse FLOAT,
            password INT
        )"""
        self.card_database.execute(card_query)
        self.card_database.commit()
        self.card_cursor.close()
        self.card_database.close()

        self.credittime_money_db = sqlite3.connect("databases/creditTime.db")
        self.creditTime_cursor = self.credittime_money_db.cursor()
        self.credittime_money_db.execute(
            f"""CREATE TABLE IF NOT EXISTS creditTime (
            login VARCHAR,
            balanse FLOAT NOT NULL DEFAULT {randint(50000, 200000)}
        )"""
        )
        self.creditTime_cursor.execute("SELECT login FROM creditTime WHERE login = ?", ["admin"])
        if self.creditTime_cursor.fetchone() is None:
            self.creditTime_cursor.execute(f"INSERT INTO creditTime(login) VALUES(?)", ["admin"])
        self.credittime_money_db.commit()
        self.creditTime_cursor.close()
        self.credittime_money_db.close()

        self.counter_show_info_about_credit = 0

    # Start main cycle
    def run(self):
        self.main_win_fidgets()
        self.window.run()

    # Main menu
    def main_win_fidgets(self):
        top_frame = Frame(self.window.root)
        bottom_frame = Frame(self.window.root)
        top_frame.pack()
        bottom_frame.pack()
        Label(top_frame, text="Компания CREDITIME", relief=RAISED, bd=3, font=("", 18), padx=10).pack(side=LEFT, pady=(100, 20))
        font_size = 12
        Button(bottom_frame, text="Войти в аккаунт", command=self.comeInAccount, font=("", font_size)).pack(side=LEFT, padx=(0, 10))
        Button(bottom_frame, text="Регистарция", command=self.registration, font=("", font_size)).pack(side=LEFT)

    # Come in account
    def comeInAccount(self):
        comeInAcc = Child_window(self.window.root, "Вход в аккаунт", 500, 500, 700, 250, "icon/comeToAcc.ico")
        title_frame = Frame(comeInAcc.root)
        title_frame.pack()
        Label(title_frame, text=f"Войти в {self.name}", relief=RAISED, bd=3, font=("", 18), padx=30).pack(side=LEFT, pady=(30, 35))

        label_phone_or_email = Frame(comeInAcc.root)
        label_phone_or_email.pack()
        Label(label_phone_or_email, text="Введите почту или телефон", font=("", 12), padx=10).pack(side=LEFT, pady=(0, 10))

        entry_phone_or_email_frame = Frame(comeInAcc.root)
        entry_phone_or_email_frame.pack()
        input_phone_or_email = Entry(entry_phone_or_email_frame, width=30, font=("", 10))
        input_phone_or_email.pack(side=LEFT, pady=(0, 10))

        label_password_frame = Frame(comeInAcc.root)
        label_password_frame.pack()
        Label(label_password_frame, text="Пароль", font=("", 12)).pack(side=LEFT, pady=(0, 10))

        entry_password_frame = Frame(comeInAcc.root)
        entry_password_frame.pack()
        input_password = Entry(entry_password_frame, width=30, font=("", 10), show="*")
        input_password.pack(side=LEFT, pady=(0, 10))

        btn_submit_frame = Frame(comeInAcc.root)
        btn_submit_frame.pack()
        Button(btn_submit_frame, text="Войти", font=("", 12), width=12, command=lambda: self.check_input_data(input_phone_or_email, input_password, comeInAcc)).pack(side=LEFT)
        comeInAcc.focus()

    # Check user data
    def check_input_data(self, input_phone_or_email=Entry, input_password=Entry, child_window=Child_window):
        examination = False
        user_id = None
        if input_phone_or_email.get() != "":
            if input_password.get() != "":
                try:
                    self.database = sqlite3.connect("databases/clients.db")
                    self.cursor = self.database.cursor()
                    self.database.create_function("md5", 1, self.md5sum)
                    email = ""
                    phone = ""
                    if input_phone_or_email.get()[0] == "+":
                        self.cursor.execute("SELECT phone FROM users WHERE phone = ?", [input_phone_or_email.get()])
                        phone = input_phone_or_email.get()
                    else:
                        self.cursor.execute("SELECT email FROM users WHERE email = ?", [input_phone_or_email.get()])
                        email = input_phone_or_email.get()
                    if self.cursor.fetchone() is None:
                        messagebox.showwarning("Логин", "Такого логина не существует")
                    else:
                        self.cursor.execute(
                            "SELECT password FROM users WHERE email = ? AND password = md5(?) OR phone = ? AND password = md5(?)",
                            [email, input_password.get(), phone, input_password.get()],
                        )
                        if self.cursor.fetchone() is None:
                            messagebox.showwarning("Пароль", "Не верный пароль!")
                        else:
                            messagebox.showinfo("Успех", "Вы успешно вошли в свой аккаунт!")
                            user_id = self.cursor.execute("SELECT id FROM users WHERE email = ? OR phone = ?", [email, phone]).fetchone()[0]
                            examination = True
                except sqlite3.Error as er:
                    print(er.with_traceback())
                    messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
                finally:
                    self.cursor.close()
                    self.database.close()
            else:
                messagebox.showwarning("Пароль", "Введите пароль!")
        else:
            messagebox.showwarning("Предупреждение", "Введите логин!")

        if examination == True:
            self.close_win.simple_close_window(child_window)
            self.client_area(user_id)

    # Client Area
    def client_area(self, user_id):
        try:
            self.database = sqlite3.connect("databases/clients.db")
            self.cursor = self.database.cursor()
            self.user.set_id(user_id)
            self.user.set_fname(self.cursor.execute("SELECT first_name FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_lname(self.cursor.execute("SELECT last_name FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_email(self.cursor.execute("SELECT email FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_password(self.cursor.execute("SELECT password FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_phone(self.cursor.execute("SELECT phone FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_age(self.cursor.execute("SELECT age FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_work_place(self.cursor.execute("SELECT work_place FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_work_position(self.cursor.execute("SELECT work_position FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_salary(self.cursor.execute("SELECT salary FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_credit(self.cursor.execute("SELECT credit FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_sum_use_credit(self.cursor.execute("SELECT sum_use_credit FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_credit_days(self.cursor.execute("SELECT credit_days FROM users WHERE id = ?", [user_id]).fetchone()[0])
            self.user.set_regula_client(self.cursor.execute("SELECT regular_client FROM users WHERE id = ?", [user_id]).fetchone()[0])
        except sqlite3.Error as er:
            print(er.with_traceback())
            messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
        finally:
            self.cursor.close()
            self.database.close()
        self.window.root.withdraw()
        client_area_window = Child_window(self.window.root, "Пользовательский кабинет", 500, 500, 800, 250, "icon/user_profile.ico")
        client_area_window.root.protocol(
            "WM_DELETE_WINDOW",
            lambda this_window=client_area_window: self.close_win.exit(this_window, "Закрыть программу?"),
        )
        main_title_frame = Frame(client_area_window.root)
        main_title_frame.pack()
        user_profile_frame = Frame(client_area_window.root)
        user_profile_frame.pack()
        credit_frame = Frame(client_area_window.root)
        credit_frame.pack()
        return_credit = Frame(client_area_window.root)
        return_credit.pack()
        exit_account = Frame(client_area_window.root)
        exit_account.pack()
        Label(main_title_frame, text="Личный кабинет", relief=RAISED, bd=3, font=("", 18), padx=30).pack(side=LEFT, pady=(30, 35))  # Заголовок
        Button(user_profile_frame, text="Профиль", width=18, font=("", 12), command=lambda: self.profile(client_area_window)).pack(side=LEFT, pady=(0, 5))
        Button(credit_frame, text="Кредитный отдел", width=18, command=lambda: self.apply_for_credit(client_area_window), font=("", 12)).pack(side=LEFT, pady=(0, 5))
        Button(return_credit, text="Вернуть кредит", width=18, command=lambda: self.return_credit(client_area_window), font=("", 12)).pack(side=LEFT, pady=(0, 5))
        Button(
            exit_account,
            text="Выйти из приложения",
            width=18,
            command=lambda this_window=client_area_window: self.close_win.exit(this_window, "Закрыть приложение?"),
            font=("", 12),
        ).pack(side=LEFT)

    # Return credit
    def return_credit(self, client_area_window=Child_window):
        if self.user.get_credit() == 0:
            messagebox.showinfo("Кредит", "У вас нету занятого кредита!")
            return
        win_return_credit = Child_window(client_area_window.root, "Возврат кредита", 600, 230, 800, 250, "icon/apply_credit.ico")
        frame_main_title = Frame(win_return_credit.root)
        frame_main_title.pack()
        frame_return_credit = Frame(win_return_credit.root)
        frame_return_credit.pack()
        frame_btn = Frame(win_return_credit.root)
        frame_btn.pack()
        try:
            self.card_database = sqlite3.connect("databases/cards.db")
            self.card_cursor = self.card_database.cursor()
            Label(frame_main_title, text="Возврат кредита", relief=RAISED, bd=3, font=("", 18), padx=30).pack(pady=(30, 20))
            Label(
                frame_return_credit,
                text=f"Вам нужно вернуть сумму занятого креда в размере: {self.user.get_credit()} грн.\n"
                + f"И также сумму за использование этого кредита в размере {self.user.get_sum_use_credit()} грн.\n"
                + f"Итоговая сумма - {self.user.get_credit() + self.user.get_sum_use_credit()} грн.\n"
                + f"Срок кредита - {self.user.get_credit_days()}\n",
                justify=LEFT,
                font=("", 11),
            ).pack(pady=(0, 0))
            Button(frame_btn, text="Вернуть кредит", command=lambda: self.pay_credit(win_return_credit), font=("", 10)).pack(side=LEFT, padx=(0, 10))
            Button(frame_btn, text="Инфо. о карет", command=lambda: self.info_about_card(win_return_credit), font=("", 10)).pack(padx=(10, 0))
        except sqlite3.Error as er:
            print(er.with_traceback())
            messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
        finally:
            self.card_cursor.close()
            self.card_database.close()
        win_return_credit.focus()

    # Pay credit
    def pay_credit(self, win_return_credit=Child_window):
        win_pay_credit = Child_window(win_return_credit.root, "Оплата", 250, 220, 800, 350, "icon/credit.ico")
        frame_main_title = Frame(win_pay_credit.root)
        frame_main_title.pack()
        frame_number_card = Frame(win_pay_credit.root)
        frame_number_card.pack(pady=(0, 10))
        frame_password_card = Frame(win_pay_credit.root)
        frame_password_card.pack()
        frame_balanse_card = Frame(win_pay_credit.root)
        frame_balanse_card.pack()
        Label(frame_main_title, text="Карта", relief=RAISED, bd=3, font=("", 14), padx=30).pack(pady=(20, 15))  # Заголовок
        Label(frame_number_card, text=f"Номер карты:", font=("", 10), padx=30).pack(pady=(0, 5))
        number_card = Entry(frame_number_card)
        number_card.pack()
        Label(frame_password_card, text=f"Пароль:", font=("", 10), padx=30).pack(pady=(0, 5))
        password_card = Entry(frame_password_card)
        password_card.pack(pady=(0, 10))
        Button(win_pay_credit.root, text="Оплатить", font=("", 10), command=lambda: self.check_pay_credit(win_return_credit, win_pay_credit, number_card, password_card)).pack()
        win_pay_credit.focus()

    # Loan payment verification
    def check_pay_credit(self, win_return_credit=Child_window, win_pay_credit=Child_window, number_card=Entry, password_card=Entry):
        if number_card.get() == "" or password_card.get() == "":
            messagebox.showwarning("Предупреждение", "Пустые поля!")
        else:
            try:
                self.database = sqlite3.connect("databases/clients.db")
                self.cursor = self.database.cursor()
                self.card_database = sqlite3.connect("databases/cards.db")
                self.card_cursor = self.card_database.cursor()
                self.credittime_money_db = sqlite3.connect("databases/creditTime.db")
                self.creditTime_cursor = self.credittime_money_db.cursor()
                if not self.is_number(number_card.get()) or not self.is_int(number_card.get()) or not self.is_number(password_card.get()) or not self.is_int(password_card.get()):
                    messagebox.showwarning("Предупреждение", "Не корректные данные")
                else:
                    self.card_cursor.execute("SELECT number_card FROM users_cards WHERE number_card = ?", [int(number_card.get())])
                    if self.card_cursor.fetchone() is None:
                        messagebox.showerror("Предупреждение", "Такого номера карыт нет!")
                    else:
                        self.card_cursor.execute("SELECT password FROM users_cards WHERE number_card = ? AND password = ?", [int(number_card.get()), int(password_card.get())])
                        if self.card_cursor.fetchone() is None:
                            messagebox.showerror("Предупреждение", "Не верный пароль")
                        else:
                            balanse = self.card_cursor.execute(
                                "SELECT balanse FROM users_cards WHERE number_card = ? AND password = ?", [int(number_card.get()), int(password_card.get())]
                            ).fetchone()[0]
                            total_sum_credit = self.user.get_credit() + self.user.get_sum_use_credit()
                            if balanse >= total_sum_credit:
                                self.card_cursor.execute("UPDATE users_cards SET balanse = balanse - ? WHERE number_card = ?", [float(total_sum_credit), int(number_card.get())])
                                self.creditTime_cursor.execute("UPDATE creditTime SET balanse = balanse + ? WHERE login = ?", [total_sum_credit, "admin"])
                                self.cursor.execute("UPDATE users SET credit = ? WHERE id = ?", [0, self.user.get_id()])
                                self.cursor.execute("UPDATE users SET sum_use_credit = ? WHERE id = ?", [0, self.user.get_id()])
                                self.cursor.execute("UPDATE users SET credit_days = ? WHERE id = ?", ["0", self.user.get_id()])
                                self.cursor.execute("UPDATE users SET regular_client = ? WHERE id = ?", [1, self.user.get_id()])
                                self.card_database.commit()
                                self.credittime_money_db.commit()
                                self.database.commit()
                                self.user.set_credit(0.0)
                                self.user.set_sum_use_credit(0.0)
                                self.user.set_credit_days(0)
                                self.user.set_regula_client(1)
                                if messagebox.showinfo("Успех", "Вы успешно вернули свой кредит!"):
                                    self.close_win.simple_close_window(win_return_credit)
                                    self.close_win.simple_close_window(win_pay_credit)
                            else:
                                messagebox.showerror("Средства", "Не карте не достаточно средств для оплаты кредита!")
                                return
            except sqlite3.Error as er:
                print(er.with_traceback())
                messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
            finally:
                self.cursor.close()
                self.database.close()
                self.card_cursor.close()
                self.card_database.close()
                self.creditTime_cursor.close()
                self.credittime_money_db.close()

    # User profile
    def profile(self, client_area_window=Child_window):
        client_area_window.root.withdraw()
        profile = Child_window(client_area_window.root, "Пользовательский кабинет", 500, 500, 800, 250, "icon/user_profile.ico")
        profile.root.protocol(
            "WM_DELETE_WINDOW",
            lambda this_window=client_area_window: self.close_win.exit(this_window, "Закрыть программу?"),
        )
        if self.user.get_work_place() == None:
            if messagebox.askokcancel(profile.root, "Необходимо заполнить некотороые данные!"):
                profile.root.withdraw()
                self.additional_information_window(profile, client_area_window)
                profile.root.destroy()
                return
            else:
                self.close_and_show_another_window(profile, client_area_window)
                return
        main_title_frame = Frame(profile.root)
        main_title_frame.pack()
        about_client = Frame(profile.root)
        about_client.pack()
        info_about_work = Frame(profile.root)
        info_about_work.pack()
        credit_frame = Frame(profile.root)
        credit_frame.pack()
        exit_this_win = Frame(profile.root)
        exit_this_win.pack()
        Label(main_title_frame, text="Профиль", relief=RAISED, bd=3, font=("", 18), padx=30).pack(pady=(20, 15))  # Заголовок
        Label(
            about_client,
            text=f"ФИО: {self.user.get_lname()}, {self.user.get_fname()}\n"
            + f"Возраст: {self.user.get_age()}\n"
            + f"Email: {self.user.get_email()}\n"
            + f"Номер телефона: {self.user.get_phone()}\n"
            + f"Место работы: {self.user.get_work_place()}\n"
            + f"Должность: {self.user.get_work_position()}\n"
            + f"Зарплата: {self.user.get_salary()} грн.",
            font=("", 12, "bold"),
            justify=LEFT,
        ).pack()
        text = ""
        if self.user.get_credit() != 0:
            text = f"Взят кредит на сумму: {self.user.get_credit()} грн\n" + f"Срок кредита: {self.user.get_credit_days()}"
        else:
            text = "Кредит не оформлен!"
        credit = Label(credit_frame, text=text, justify=LEFT, font=("", 12, "bold"))
        credit.pack()
        Button(exit_this_win, text="В личный кабинет", font=("", 12), command=lambda: self.close_and_show_another_window(profile, client_area_window)).pack(
            side=LEFT, padx=(0, 5), pady=(40, 15)
        )
        Button(exit_this_win, text="Инфо. о карте", font=("", 12), command=lambda: self.info_about_card(profile)).pack(side=LEFT, padx=(5, 5), pady=(40, 15))
        Button(exit_this_win, text="Баланс на карте", font=("", 12), command=lambda: self.info_about_balanse_card(profile)).pack(padx=(5, 0), pady=(40, 15))
        Button(profile.root, text="Выйти из аккаунта", font=("", 12), command=lambda: self.close_win.exit_account(profile, client_area_window)).pack()

    # Balanse card
    def info_about_balanse_card(self, profile=Child_window):
        info_about_balanse_card = Child_window(profile.root, "Баланс на карте", 250, 300, 800, 350, "icon/credit.ico")
        frame_main_title = Frame(info_about_balanse_card.root)
        frame_main_title.pack()
        frame_number_card = Frame(info_about_balanse_card.root)
        frame_number_card.pack(pady=(0, 10))
        frame_password_card = Frame(info_about_balanse_card.root)
        frame_password_card.pack()
        frame_balanse_card = Frame(info_about_balanse_card.root)
        frame_balanse_card.pack()
        Label(frame_main_title, text="Баланс", relief=RAISED, bd=3, font=("", 14), padx=30).pack(pady=(20, 15))  # Заголовок
        Label(frame_number_card, text=f"Номер карты:", font=("", 10), padx=30).pack(pady=(0, 5))
        number_card = Entry(frame_number_card)
        number_card.pack()
        Label(frame_password_card, text=f"Пароль:", font=("", 10), padx=30).pack(pady=(0, 5))
        password_card = Entry(frame_password_card)
        password_card.pack()
        label_balanse = Label()
        balanse = "Нажмите кнопу посмотреть"
        if self.user.get_number_card() != None:
            number_card.insert(0, self.user.get_number_card())
            password_card.insert(0, self.user.get_password_card())

        label_balanse = Label(frame_balanse_card, text=f"Баланс: {balanse}")
        label_balanse.pack(pady=(5, 5))
        Button(info_about_balanse_card.root, text="Посмотреть баланс", command=lambda: self.show_balanse(label_balanse, number_card, password_card)).pack(pady=(0, 10))
        Button(info_about_balanse_card.root, text="Закрыть окно", command=lambda: self.close_win.simple_close_window(info_about_balanse_card)).pack()

    # Show info about balance on card
    def show_balanse(self, label_balanse=Label, number_card=Entry, password_card=Entry):
        if number_card.get() == "" or password_card.get() == "":
            messagebox.showwarning("Предупреждение", "Пустые поля!")
        else:
            try:
                self.card_database = sqlite3.connect("databases/cards.db")
                self.card_cursor = self.card_database.cursor()
                if not self.is_number(number_card.get()) or not self.is_int(number_card.get()) or not self.is_number(password_card.get()) or not self.is_int(password_card.get()):
                    messagebox.showwarning("Предупреждение", "Не корректные данные")
                else:
                    self.card_cursor.execute("SELECT number_card FROM users_cards WHERE number_card = ?", [int(number_card.get())])
                    if self.card_cursor.fetchone() is None:
                        messagebox.showerror("Предупреждение", "Такого номера карыт нет!")
                    else:
                        self.card_cursor.execute("SELECT password FROM users_cards WHERE number_card = ? AND password = ?", [int(number_card.get()), int(password_card.get())])
                        if self.card_cursor.fetchone() is None:
                            messagebox.showerror("Предупреждение", "Не верный пароль")
                        else:
                            self.user.set_number_card(int(number_card.get()))
                            self.user.set_password_card(int(password_card.get()))
                            balanse = self.card_cursor.execute(
                                "SELECT balanse FROM users_cards WHERE number_card = ? AND password = ?", [int(number_card.get()), int(password_card.get())]
                            ).fetchone()[0]
                            money = f"Баланс на карте: {balanse} грн."
                            label_balanse["text"] = money
            except sqlite3.Error as er:
                print(er.with_traceback())
                messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
            finally:
                self.card_cursor.close()
                self.card_database.close()

    def info_about_card(self, profile=Child_window):
        win_info_card = Child_window(profile.root, "Инфо. о карте", 250, 170, 800, 350, "icon/credit.ico")
        try:
            self.card_database = sqlite3.connect("databases/cards.db")
            self.card_cursor = self.card_database.cursor()
            number_card = self.card_cursor.execute("SELECT number_card FROM users_cards WHERE number_card = ?", [self.user.get_id()]).fetchone()[0]
            password_card = self.card_cursor.execute("SELECT password FROM users_cards WHERE number_card = ?", [self.user.get_id()]).fetchone()[0]
            Label(win_info_card.root, text="Карта", relief=RAISED, bd=3, font=("", 14), padx=30).pack(pady=(20, 15))  # Заголовок
            Label(win_info_card.root, text=f"Номер карты: {number_card}", font=("", 10), padx=30).pack(pady=(0, 5))
            Label(win_info_card.root, text=f"Пароль: {password_card}", font=("", 10), padx=30).pack(pady=(0, 10))
            Button(win_info_card.root, text="ОК", command=lambda: self.close_win.simple_close_window(win_info_card)).pack()
        except sqlite3.Error as er:
            print(er.with_traceback())
            messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
        finally:
            self.card_cursor.close()
            self.card_database.close()

    def additional_information_window(self, profile_window=Child_window, client_area_window=Child_window):
        add_info_win = Child_window(profile_window.root, "Доп. информация о клиенте", 400, 200, 800, 350, "icon/add_info.ico")
        main_title_frame = Frame(add_info_win.root)
        main_title_frame.pack()
        work_place_frame = Frame(add_info_win.root)
        work_place_frame.pack()
        work_position_frame = Frame(add_info_win.root)
        work_position_frame.pack()
        salary_frame = Frame(add_info_win.root)
        salary_frame.pack()
        button_frame = Frame(add_info_win.root)
        button_frame.pack()
        Label(main_title_frame, text="Заполните доп. данные", relief=RAISED, bd=3, font=("", 14), padx=30).pack(side=LEFT, pady=(15, 15))  # Заголовок
        Label(work_place_frame, text="Место работы:", font=("", 11)).pack(side=LEFT, padx=(0, 0))
        work_place = Entry(work_place_frame, font=("", 11))
        work_place.pack(side=LEFT, padx=(5, 23))  # first name
        Label(work_position_frame, text="Должность:", font=("", 11)).pack(side=LEFT, padx=(0, 0))
        work_position = Entry(work_position_frame, font=("", 11))
        work_position.pack(side=LEFT, padx=(5, 0))

        Label(salary_frame, text="Зарплата:", font=("", 11)).pack(side=LEFT, padx=(10, 0))
        salary = Entry(salary_frame, font=("", 11))
        salary.pack(side=LEFT, padx=(5, 0))
        Button(
            button_frame, text="Ок", command=lambda: self.check_input_user(work_place.get(), work_position.get(), salary.get(), add_info_win, profile_window, client_area_window)
        ).pack(side=LEFT, padx=(0, 5), pady=(15, 0))
        Button(button_frame, text="Отмена", command=lambda: self.close_and_show_another_window(add_info_win, client_area_window)).pack(side=LEFT, padx=(5, 0), pady=(15, 0))
        add_info_win.focus()

    def check_input_user(self, work_place, work_position, salary, win=Child_window, profile_window=Child_window, client_area_window=Child_window):
        if work_place == "" or work_position == "" or salary == "":
            messagebox.showwarning("Предупреждение", "Не все данные введенный")
        else:
            if not self.is_number(salary):
                messagebox.showwarning("Ошбика", "Не корректный тип данных")
            elif float(salary) < 6500:
                messagebox.showwarning("Не корректные данные", "Минимальная зарпалата в Украине 6500 грн.")
            else:
                try:
                    self.database = sqlite3.connect("databases/clients.db")
                    self.cursor = self.database.cursor()
                    self.user.set_work_place(work_place)
                    self.user.set_work_position(work_position)
                    self.user.set_salary(float(salary))
                    self.cursor.execute(
                        "UPDATE users SET work_place = ?, work_position = ?, salary = ? WHERE id = ?", [work_place, work_position, float(salary), self.user.get_id()]
                    )
                    self.database.commit()
                    messagebox.showinfo("Успех", "Мы успешно занесли данные.\n Снова зайдите в профиль!")
                    self.close_win.simple_close_window(win)
                    client_area_window.root.deiconify()
                except sqlite3.Error as er:
                    print(er.with_traceback())
                    messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
                finally:
                    self.cursor.close()
                    self.database.close()

    def apply_for_credit(self, client_area_window=Child_window):
        aplly_credit = Child_window(client_area_window.root, "Оформление кредита", 500, 500, 800, 250, "icon/apply_credit.ico")
        aplly_credit.root.protocol(
            "WM_DELETE_WINDOW",
            lambda this_window=client_area_window: self.close_win.exit(this_window, "Закрыть программу?"),
        )

        if self.user.get_work_place() == "":
            if messagebox.showwarning("Предпреждение", "Нету необходимых данных!\nЗаполните их в профиле"):
                self.close_win.simple_close_window(aplly_credit)
        else:
            client_area_window.root.withdraw()
            frame_main_title = Frame(aplly_credit.root)
            frame_main_title.pack()
            frame_credit = Frame(aplly_credit.root)
            frame_credit.pack(pady=(0, 10))
            frame_days_credit = Frame(aplly_credit.root)
            frame_days_credit.pack(padx=(10, 0))
            frame_about_credit = Frame(aplly_credit.root)
            frame_about_credit.pack()
            Label(frame_main_title, text="Кредитный отдел", relief=RAISED, bd=3, font=("", 18), padx=30).pack(pady=(30, 20))

            Label(frame_credit, text="Сумма кредита:").pack(side=LEFT, padx=(0, 5))
            sum_credit = Entry(frame_credit, text="Credit")
            sum_credit.pack(pady=(2, 0))
            Label(frame_days_credit, text="Срок кредита:").pack(side=LEFT, padx=(0, 5))
            month = ""
            if self.user.get_regula_client() == 1:
                month = ("1 месяц", "2 месяца", "3 месяца", "4 месяца", "5 месяцев", "6 месяцев", "7 месяцев", "8 месяцев", "9 месяцев")
            else:
                month = ("1 месяц", "2 месяца", "3 месяца")
            days = Combobox(frame_days_credit, width=17, justify=CENTER, values=month)
            days.current(0)
            days.pack()
            Button(frame_about_credit, text="О кредите", command=self.info_about_credit, font=("", 12)).pack(side=LEFT, padx=(0, 5), pady=(25, 0))
            Button(frame_about_credit, text="Расчёты", command=lambda: self.count_sum_credit(sum_credit, days, aplly_credit), font=("", 12)).pack(padx=(5, 0), pady=(25, 0))
            Button(aplly_credit.root, text="Оформить кредит", command=lambda: self.confirm_credit(aplly_credit, sum_credit, days), font=("", 12)).pack(padx=(5, 0), pady=(15, 0))
            Button(
                aplly_credit.root, text="В личный кабинет", font=("", 12), command=lambda: self.close_and_show_another_window(aplly_credit, client_area_window, sum_credit)
            ).pack(padx=(5, 0), pady=(15, 0))

        if self.counter_show_info_about_credit == 0:
            self.info_about_credit()
            self.counter_show_info_about_credit += 1

    def confirm_credit(self, aplly_credit=Child_window, sum_credit=Entry, month=Combobox):
        if self.user.get_work_place() == None:
            messagebox.showerror("Нету необходимых данных!", "Заполните данные в своём профиле!")
            return
        if self.user.get_credit() > 0:
            messagebox.showinfo("Кредит", "У вас есть не погашенный кредит!")
        else:
            if sum_credit.get() == "":
                messagebox.showwarning("Предупреждение", "Пустое поле!")
                return
            else:
                if not self.is_number(sum_credit.get()):
                    messagebox.showwarning("Предупреждение", "Не корректный в вод данных!")
                    return
                else:
                    summa = float(sum_credit.get())
                    how_months = int(month.get()[0])
                    percent_one_day = (float(summa) * 2) / 100
                    sum_for_use_credit = percent_one_day * (how_months * 30)
                    total = summa + sum_for_use_credit
                    if summa < 600:
                        messagebox.showwarning("Предупреждение", "Минимальная сумма 600 гнр.")
                        return
                    elif summa > 15000 and self.user.get_regula_client() == 0:
                        messagebox.showwarning(
                            "Клиенту",
                            "Вы не постоянный клиент, вам разрешена сумма до 15 000 грн.\nПогасив кредит, вы станете постоянным клиетом и сможете оформить следующий кредит до 25 000 грн.",
                        )
                        return
                    elif summa > 25000 and self.user.get_regula_client() == 1:
                        messagebox.showwarning("Клиенту", "Наша компания выдает кредит максимально до 25 000 грн.")
                        return
                    elif total > self.user.get_salary() * how_months:
                        messagebox.showwarning("Средства", "Ваша зарплата не способна погасить кредит выберите меньшую сумму.")
                        return
            win_con_credit = Child_window(aplly_credit.root, "Договор", 350, 250, 800, 350, "icon/apply_credit.ico")
            Label(win_con_credit.root, text="Подтвержение кредита", relief=RAISED, bd=3, font=("", 18), padx=30).pack(pady=(30, 20))
            user_card = Frame(win_con_credit.root)
            user_card.pack()
            Label(user_card, text="Номер карты:").pack(side=LEFT, padx=(0, 5))
            number_card = Entry(user_card)
            number_card.pack(pady=(2, 0))
            Button(win_con_credit.root, text="Подтвердить кредит", command=lambda: self.confirm_credit1(win_con_credit, number_card, sum_credit, month)).pack(pady=(10, 0))
            win_con_credit.focus()

    def confirm_credit1(self, win=Child_window, number_card=Entry, summa=Entry, months=Combobox):
        if number_card.get() == "":
            messagebox.showwarning("Предупреждение", "Пустое поле!")
        else:
            if not self.is_number(number_card.get()) or not self.is_int(number_card.get()):
                messagebox.showwarning("Ошибка", "Не корректный в вод данных")
            else:
                try:
                    self.card_database = sqlite3.connect("databases/cards.db")
                    self.card_cursor = self.card_database.cursor()
                    self.database = sqlite3.connect("databases/clients.db")
                    self.cursor = self.database.cursor()
                    self.card_cursor.execute("SELECT balanse FROM users_cards WHERE number_card = ?", [int(number_card.get())])
                    if not self.card_cursor.fetchone():
                        messagebox.showwarning("Запрос не найден", "Карта с таким номером не найдена!")
                    else:
                        if messagebox.askokcancel("Важно", "Отменить операцию будет нельзя!"):
                            how_months = int(months.get()[0])
                            percent_one_day = (float(summa.get()) * 2) / 100
                            sum_for_use_credit = percent_one_day * (how_months * 30)
                            self.user.set_credit_days(months.get())
                            self.user.set_sum_use_credit(sum_for_use_credit)
                            self.user.set_credit(float(summa.get()))
                            self.card_cursor.execute("UPDATE users_cards SET balanse = balanse + ? WHERE number_card = ?", [float(summa.get()), int(number_card.get())])
                            self.cursor.execute(
                                "UPDATE users SET credit = ?, sum_use_credit = ?, credit_days = ? WHERE id = ?",
                                [self.user.get_credit(), self.user.get_sum_use_credit(), months.get(), self.user.get_id()],
                            )
                            self.card_database.commit()
                            self.database.commit()
                            messagebox.showinfo("Операция завершенна", "Вы получили деньги на свою карту!")
                            self.close_win.simple_close_window(win)
                except sqlite3.Error as er:
                    print(er.with_traceback())
                    messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
                finally:
                    self.card_cursor.close()
                    self.card_database.close()
                    self.cursor.close()
                    self.database.close()

    def info_about_credit(self):
        info_credit = """Минмальная сумма кредита - 600 грн.
Максимальная сумма кредита - 15 000 грн для не постоянного клиента.
Для постоянного клиента доступна сумма кредита в размере 25 000 грн.
Кредитный процент составляет 2% на день.
Срок платежа для не постоянных клиетов от 1 до 3 месяцев.
Для постоянного клиента срок составляет до 9 месяцев."""
        messagebox.showinfo("О кредите", info_credit)

    def count_sum_credit(self, sum_credit=Entry, month=Combobox, aplly_credit=Child_window):
        if sum_credit.get() != "":
            if not self.is_number(sum_credit.get()):
                messagebox.showerror("Ошибка", "Не корректный тип данных")
                return
            else:
                summa = float(sum_credit.get())
                how_months = int(month.get()[0])
                if summa < 600:
                    messagebox.showwarning("Предупреждение", "Минимальная сумма 600 гнр.")
                elif summa > 15000 and self.user.get_regula_client() == 0:
                    messagebox.showwarning(
                        "Клиенту",
                        "Вы не постоянный клиент, вам разрешена сумма до 15 000 грн.\nПогасив кредит, вы станете постоянным клиетом и сможете оформить следующий кредит до 25 000 грн.",
                    )
                elif summa > 25000 and self.user.get_regula_client() == 1:
                    messagebox.showwarning("Клиенту", "Наша компания выдает кредит максимально до 25 000 грн.")
                else:
                    total_about_credit = Child_window(aplly_credit.root, "Итоги по кредиту", 600, 300, 800, 250, "icon/apply_credit.ico")
                    frame_main_title = Frame(total_about_credit.root)
                    frame_main_title.pack()
                    frame_credit_without_percent = Frame(total_about_credit.root)
                    frame_credit_without_percent.pack()
                    frame_time_credit = Frame(total_about_credit.root)
                    frame_time_credit.pack()
                    frame_percent = Frame(total_about_credit.root)
                    frame_percent.pack()
                    frame_percent_for_one_day = Frame(total_about_credit.root)
                    frame_percent_for_one_day.pack()
                    Label(frame_main_title, text="Итоги по кредиту", relief=RAISED, bd=3, font=("", 18), padx=30).pack(pady=(30, 20))
                    Label(
                        frame_credit_without_percent,
                        justify=LEFT,
                        font=("", 12),
                        text=f"Сумма кредита без учёта процентов: {summa} грн.\n" + f"Кредит выдается на: {month.get()}\n" + f"Ежедневная процентная ставка: 2%",
                    ).pack()
                    percent_one_day = (summa * 0.5) / 100
                    sum_for_use_credit = percent_one_day * (how_months * 30)

                    total_sum = summa + sum_for_use_credit
                    Label(
                        frame_percent_for_one_day,
                        justify=LEFT,
                        font=("", 12),
                        text=f"Сумма процент за 1 день: {percent_one_day} грн.\n"
                        + f"Процент за использование кредита за {month.get()} составляет {sum_for_use_credit} грн.\n"
                        + f"С учётом использования кредина нужно будет вернуть {total_sum} грн.",
                    ).pack()
                    Button(total_about_credit.root, text="ОК", command=lambda: self.close_win.simple_close_window(total_about_credit)).pack(pady=(10, 0))
        else:
            messagebox.showwarning("Предупреждение", "Пустое поле!")
            return

    def registration(self):
        self.window.root.withdraw()
        regis = Child_window(self.window.root, "Регистрация", 500, 500, 800, 250, "icon/registration.ico")
        regis.root.protocol("WM_DELETE_WINDOW", lambda this_window=regis: self.close_win.exit(this_window, "Закрыть программу?"))
        # Вернуться в меню
        Label(regis.root, text=f"Создание аккаунта в {self.name}", relief=RAISED, bd=3, font=("", 18), padx=10).place(
            relx=0.5,
            rely=0.1,
            anchor=CENTER,
        )  # Заголовок

        Label(regis.root, text="Имя").place(relx=0.337, rely=0.2, anchor=CENTER)
        first_name = Entry(regis.root)
        first_name.place(relx=0.5, rely=0.2, anchor=CENTER)  # first name
        Label(regis.root, text="Фамилия").place(relx=0.31, rely=0.25, anchor=CENTER)
        last_name = Entry(regis.root)
        last_name.place(relx=0.5, rely=0.25, anchor=CENTER)  # last name
        Label(regis.root, text="email").place(relx=0.33, rely=0.30, anchor=CENTER)
        email = Entry(regis.root)
        email.place(relx=0.5, rely=0.30, anchor=CENTER)  # email
        Label(regis.root, text="Пароль").place(relx=0.32, rely=0.35, anchor=CENTER)
        password = Entry(regis.root, show="*")
        password.place(relx=0.5, rely=0.35, anchor=CENTER)  # password
        Label(regis.root, text="Повторите пароль").place(relx=0.26, rely=0.40, anchor=CENTER)
        repeat_password = Entry(regis.root, show="*")
        repeat_password.place(relx=0.5, rely=0.40, anchor=CENTER)  # repeat_pass
        Label(regis.root, text="Телефон: +380").place(relx=0.282, rely=0.45, anchor=CENTER)
        phone = Entry(regis.root)
        phone.place(relx=0.5, rely=0.45, anchor=CENTER)  # phone
        Label(regis.root, text="Возраст").place(relx=0.315, rely=0.50, anchor=CENTER)
        age = Spinbox(regis.root, from_=18, to=60, width=4)
        age.place(relx=0.414, rely=0.50, anchor=CENTER)
        Button(regis.root, text="Очистить поля", command=lambda: self.clear([first_name, last_name, email, password, repeat_password, phone, age])).place(
            relx=0.55, rely=0.50, anchor=CENTER
        )
        Button(regis.root, text="Зарегистрироваться", command=lambda: self.get_info(first_name, last_name, email, password, repeat_password, phone, age)).place(
            relx=0.33, rely=0.58, anchor=CENTER
        )
        title = "Закрыть окно регистрации"
        question = "Вернуться в меню?"
        Button(
            regis.root,
            text="Вернуться в меню",
            command=lambda this_window=regis: self.close_window(this_window, title, question),
        ).place(relx=0.63, rely=0.58, anchor=CENTER)

    def clear(self, entries=[]):
        if type(entries[0] == Entry):
            for data in entries:
                data.delete(0, END)
        else:
            print("Error type")

    def get_info(self, fname=Entry, lname=Entry, email=Entry, password=Entry, repeat_password=Entry, phone=Entry, age=Spinbox):
        if fname.get() != "" and lname.get() != "" and email.get() != "" and password.get() != "" and repeat_password.get() != "" and phone.get() != "" and age.get() != "":
            # check email========================
            email_str = str(email.get())
            correct_email = False
            unValidSumbol = "-+!@#$%^&*()|\?/<>~\"'"
            for i in range(len(email_str)):
                if email_str[0] == "@":
                    correct_email = False
                    break
                else:
                    if email_str[i] == "@":
                        symbol = email_str[:i]
                        if self.check_email(symbol, unValidSumbol) == True:
                            messagebox.showwarning("Символы", "Могут использоваться символы (a-z), цифры (0-9) и точку.")
                            return
                        if len(symbol) < 6:
                            print(symbol)
                            break
                        elif len(symbol) >= 8:
                            alphaValid = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            alphaValid += alphaValid.lower()
                            if self.check_email(symbol, alphaValid) == False:
                                break
                        if email_str[i + 1 :] == "gmail.com" or email_str[i + 1 :] == "mail.ru" or email_str[i + 1 :] == "yandex.ru":
                            correct_email = True
                            break
                    else:
                        correct_email = False
            if correct_email == False:
                messagebox.showerror("Не корректные данные", "Не правильная почта!")
                return
            # ===================================
            # Check password
            if len(password.get()) < 4:
                messagebox.showwarning("Пароль", "Пароль должен содержать минимум 4 символа")
                return
            if password.get() != repeat_password.get():
                messagebox.showwarning("Предупреждение", "Пароли не совпадают!")
                return
            # ====================================
            # check phone
            validSymbols = "1234567890"
            if not self.check_phone(phone.get(), validSymbols):
                messagebox.showwarning("Телефон", "Не корректный номер телефона")
                return
            # =====================================
            # check age
            str_age = age.get()
            for val in str_age:
                if not (val in validSymbols):
                    messagebox.showerror("Ошибка", "Введены не корректные данные!")
                    return
            if int(str_age) < 18 or int(str_age) > 60:
                messagebox.showwarning("Возрастные ограничения", "Наша компанию обслуживает людей возрастом от 18 до 60 лет включительно!")
                return
            # =====================================

            try:
                self.database = sqlite3.connect("databases/clients.db")
                self.cursor = self.database.cursor()
                self.database.create_function("md5", 1, self.md5sum)
                self.cursor.execute(f"SELECT email FROM users WHERE email = '{email.get()}'")
                if self.cursor.fetchone() is None:
                    user_phone = "+380" + phone.get()
                    self.cursor.execute(f"SELECT phone FROM users WHERE phone = '{user_phone}'")
                    if self.cursor.fetchone() is None:
                        values = [fname.get(), lname.get(), email.get(), password.get(), "+380" + phone.get(), int(age.get())]
                        self.cursor.execute("INSERT INTO users(first_name, last_name, email, password, phone, age) VALUES(?, ?, ?, md5(?), ?, ?)", values)
                        self.database.commit()
                        messagebox.showinfo("Успех", "Поздравляю вы зарегистрировались!")
                        self.card_database = sqlite3.connect("databases/cards.db")
                        self.card_cursor = self.card_database.cursor()
                        id = self.cursor.execute("SELECT id FROM users WHERE email = ?", [email.get()]).fetchone()[0]
                        self.card_cursor.execute("INSERT INTO users_cards(number_card, password, balanse) VALUES(?, ?, ?)", [id, randint(1000, 10000), randint(15000, 70000)])
                        self.clear([fname, lname, email, password, repeat_password, phone, age])
                        self.card_database.commit()
                        self.card_cursor.close()
                        self.card_database.close()
                    else:
                        messagebox.showerror("Предупреждение", "Такай номер телефона уже зарегистрирован!")
                else:
                    messagebox.showerror("Предупреждение", "Такая почта уже зарегистрированна!")
            except sqlite3.Error as er:
                print(er.with_traceback())
                messagebox.showerror("Ошибка!", "При работе с базой данный случилась не предвиденная ошибка!")
            finally:
                self.cursor.close()
                self.database.close()
        else:
            messagebox.showwarning("Данные", "Не все данные заполнены!")

    def close_window(self, this_window, title, question):
        if messagebox.askyesno(title, question):
            self.window.root.deiconify()
            this_window.root.destroy()

    def close_and_show_another_window(self, close, show, frame_clear=Entry):
        if type(frame_clear) == Entry:
            frame_clear.delete(0, END)
        show.root.deiconify()
        close.root.destroy()

    def check_phone(self, testS=str, validSymbols=str()):
        flag = True
        if len(testS) < 9 or len(testS) > 9:
            return False
        for val in testS:
            if not (val in validSymbols):
                flag = False
                break
        if flag == True:
            return True
        else:
            return False

    def check_email(self, testS=str, validSymbols=str()):
        flag = False
        for val in testS:
            if val in validSymbols:
                flag = True
                break
        if flag == True:
            return True
        else:
            return False

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def is_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def md5sum(self, value):
        return hashlib.md5(value.encode()).hexdigest()
