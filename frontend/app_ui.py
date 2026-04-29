import tkinter as tk
from tkinter import messagebox, filedialog
import os

from backend.lcg_generator import LinearCongruentialGenerator
from backend.cesaro_tester import CesaroTester
from backend.md5_algorithm import MD5
from backend.rc5_algorithm import RC5FileProtector
from backend.rsa_algorithm import RSAFileProtector
from backend.dss_algorithm import DSSProtector

class InfoSecApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Захист інформації: Лабораторні роботи")
        self.geometry("650x750")

        self.main_frame = tk.Frame(self)
        self.lab1_frame = tk.Frame(self)
        self.lab2_frame = tk.Frame(self)
        self.lab3_frame = tk.Frame(self)
        self.lab4_frame = tk.Frame(self)
        self.lab5_frame = tk.Frame(self)

        self.init_main_menu()
        self.init_lab1_ui()
        self.init_lab2_ui()
        self.init_lab3_ui()
        self.init_lab4_ui()
        self.init_lab5_ui()

        self.show_main_menu()

    def init_main_menu(self):
        tk.Label(self.main_frame, text="Головне меню", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self.main_frame, text="Лабораторна №1: ГПВЧ", command=self.show_lab1, width=30, height=2).pack(pady=10)
        tk.Button(self.main_frame, text="Лабораторна №2: MD5", command=self.show_lab2, width=30, height=2).pack(pady=10)
        tk.Button(self.main_frame, text="Лабораторна №3: RC5", command=self.show_lab3, width=30, height=2).pack(pady=10)
        tk.Button(self.main_frame, text="Лабораторна №4: RSA", command=self.show_lab4, width=30, height=2).pack(pady=10)
        tk.Button(self.main_frame, text="Лабораторна №5: DSS", command=self.show_lab5, width=30, height=2).pack(pady=10)

    def show_main_menu(self):
        self.lab1_frame.pack_forget()
        self.lab2_frame.pack_forget()
        self.lab3_frame.pack_forget()
        self.lab4_frame.pack_forget()
        self.lab5_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.update_idletasks()

    def init_lab1_ui(self):
        tk.Label(self.lab1_frame, text="Лабораторна 1: ГПВЧ", font=("Arial", 14, "bold")).pack(pady=10)

        input_frame = tk.Frame(self.lab1_frame)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Кількість чисел для генерації:").pack(side=tk.LEFT, padx=5)
        self.count_entry = tk.Entry(input_frame, width=15)
        self.count_entry.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self.lab1_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Згенерувати та Протестувати", command=self.run_lab1, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Зберегти у файл", command=self.save_to_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Назад до меню", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

        self.result_text = tk.Text(self.lab1_frame, height=20, width=75, state=tk.DISABLED)
        self.result_text.pack(pady=10)

        self.last_generated_data = ""

    def show_lab1(self):
        self.main_frame.pack_forget()
        self.lab2_frame.pack_forget()
        self.lab3_frame.pack_forget()
        self.lab4_frame.pack_forget()
        self.lab5_frame.pack_forget()
        self.lab1_frame.pack(fill="both", expand=True)
        self.update_idletasks()

    def run_lab1(self):
        count_str = self.count_entry.get()

        try:
            count = int(count_str)
            if count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Помилка вводу", "Введіть ціле додатне число")
            return

        generator = LinearCongruentialGenerator()
        sequence = generator.generate_sequence(count)
        period = generator.find_period()

        prob, pi_est = CesaroTester.test_sequence(sequence)
        sys_prob, sys_pi_est = CesaroTester.test_system_generator(count)

        output = f"Згенеровано {count} чисел\n"
        output += f"Перші 10 чисел: {sequence[:10]}...\n"
        output += f"Період генератора: {period}\n\n"

        output += "Тест Чезаро (Мій генератор)\n"
        output += f"Ймовірність взаємної простоти: {prob:.4f}\n"
        output += f"Оцінка числа pi: {pi_est:.4f}\n\n"

        output += "Тест Чезаро (Генератор від Python)\n"
        output += f"Ймовірність взаємної простоти: {sys_prob:.4f}\n"
        output += f"Оцінка числа pi: {sys_pi_est:.4f}\n\n"

        output += "Повна послідовність:\n" + str(sequence)

        self.last_generated_data = output

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, output)
        self.result_text.config(state=tk.DISABLED)

    def save_to_file(self):
        if not self.last_generated_data:
            messagebox.showwarning("Увага", "Немає даних для збереження. Спочатку згенеруйте послідовність")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                                                title="Зберегти результати")

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(self.last_generated_data)
                messagebox.showinfo("Успіх", "Дані успішно збережено")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

    def init_lab2_ui(self):
        tk.Label(self.lab2_frame, text="Лабораторна 2: Хешування MD5", font=("Arial", 14, "bold")).pack(pady=10)

        text_frame = tk.Frame(self.lab2_frame)
        text_frame.pack(pady=5)
        tk.Label(text_frame, text="Текст для хешування:").pack(side=tk.LEFT, padx=5)
        self.text_entry = tk.Entry(text_frame, width=40)
        self.text_entry.pack(side=tk.LEFT, padx=5)

        file_frame = tk.Frame(self.lab2_frame)
        file_frame.pack(pady=5)
        self.file_path_var = tk.StringVar()
        tk.Button(file_frame, text="Вибрати файл...", command=self.select_file_lab2).pack(side=tk.LEFT, padx=5)

        file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, width=35, state='readonly')
        file_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="X", command=lambda: self.file_path_var.set(""), fg="red").pack(side=tk.LEFT)

        check_frame = tk.Frame(self.lab2_frame)
        check_frame.pack(pady=5)
        tk.Label(check_frame, text="Еталонний MD5:").pack(side=tk.LEFT, padx=5)
        self.expected_hash_entry = tk.Entry(check_frame, width=35)
        self.expected_hash_entry.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self.lab2_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Обчислити та Перевірити", command=self.run_lab2, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Зберегти у файл", command=self.save_lab2_to_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Назад до меню", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

        self.lab2_result_text = tk.Text(self.lab2_frame, height=15, width=75, state=tk.DISABLED)
        self.lab2_result_text.pack(pady=10)
        self.lab2_last_data = ""

    def show_lab2(self):
        self.main_frame.pack_forget()
        self.lab1_frame.pack_forget()
        self.lab3_frame.pack_forget()
        self.lab4_frame.pack_forget()
        self.lab5_frame.pack_forget()
        self.lab2_frame.pack(fill="both", expand=True)
        self.update_idletasks()

    def select_file_lab2(self):
        filepath = filedialog.askopenfilename(title="Виберіть файл для хешування")
        if filepath:
            self.file_path_var.set(filepath)

    def run_lab2(self):
        text_input = self.text_entry.get()
        filepath = self.file_path_var.get()
        expected_hash = self.expected_hash_entry.get().strip().lower()

        if not text_input and not filepath:
            messagebox.showwarning("Помилка", "Введіть текст або виберіть файл")
            return

        output = "Результати хешування MD5\n\n"

        if text_input:
            text_hash = MD5.hash_data(text_input.encode('utf-8'))
            output += f"Текст: '{text_input}'\n"
            output += f"MD5 Хеш: {text_hash}\n"
            if expected_hash:
                match = "ЗБІГАЄТЬСЯ" if text_hash == expected_hash else "НЕ ЗБІГАЄТЬСЯ"
                output += f"Перевірка цілісності: {match}\n"

        if filepath:
            try:
                file_hash = MD5.hash_file(filepath)
                filename = os.path.basename(filepath)
                output += f"Файл: {filename}\n"
                output += f"MD5 Хеш: {file_hash}\n"
                if expected_hash:
                    match = "ЗБІГАЄТЬСЯ (Цілісність підтверджено)" if file_hash == expected_hash else "НЕ ЗБІГАЄТЬСЯ (Файл змінено або пошкоджено)"
                    output += f"Перевірка цілісності: {match}\n"
            except Exception as e:
                output += f"Помилка читання файлу: {str(e)}\n"

        self.lab2_last_data = output
        self.lab2_result_text.config(state=tk.NORMAL)
        self.lab2_result_text.delete(1.0, tk.END)
        self.lab2_result_text.insert(tk.END, output)
        self.lab2_result_text.config(state=tk.DISABLED)

    def save_lab2_to_file(self):
        if not self.lab2_last_data:
            messagebox.showwarning("Помилка", "Немає даних для збереження")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.lab2_last_data)
                messagebox.showinfo("Успіх", "Результати успішно збережено")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

    def init_lab3_ui(self):
        tk.Label(self.lab3_frame, text="Лабораторна 3: Шифрування файлів (RC5)", font=("Arial", 14, "bold")).pack(pady=10)

        pass_frame = tk.Frame(self.lab3_frame)
        pass_frame.pack(pady=5)
        tk.Label(pass_frame, text="Парольна фраза:").pack(side=tk.LEFT, padx=5)
        self.password_entry = tk.Entry(pass_frame, width=30, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5)

        file_frame = tk.Frame(self.lab3_frame)
        file_frame.pack(pady=15)
        self.lab3_file_path_var = tk.StringVar()
        tk.Button(file_frame, text="Вибрати файл", command=self.select_file_lab3).pack(side=tk.LEFT, padx=5)

        file_entry = tk.Entry(file_frame, textvariable=self.lab3_file_path_var, width=40, state='readonly')
        file_entry.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self.lab3_frame)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Зашифрувати файл", command=lambda: self.run_lab3("encrypt"), bg="lightgreen", width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Розшифрувати файл", command=lambda: self.run_lab3("decrypt"), bg="lightcoral", width=20).pack(side=tk.LEFT, padx=10)

        tk.Button(self.lab3_frame, text="Назад до меню", command=self.show_main_menu).pack(pady=20)

        self.lab3_log_text = tk.Text(self.lab3_frame, height=10, width=75, state=tk.DISABLED)
        self.lab3_log_text.pack(pady=10)

    def show_lab3(self):
        self.main_frame.pack_forget()
        self.lab1_frame.pack_forget()
        self.lab2_frame.pack_forget()
        self.lab4_frame.pack_forget()
        self.lab5_frame.pack_forget()
        self.lab3_frame.pack(fill="both", expand=True)
        self.update_idletasks()

    def select_file_lab3(self):
        filepath = filedialog.askopenfilename(title="Виберіть файл для шифрування/дешифрування")
        if filepath:
            self.lab3_file_path_var.set(filepath)

    def log_lab3(self, message):
        self.lab3_log_text.config(state=tk.NORMAL)
        self.lab3_log_text.insert(tk.END, message + "\n")
        self.lab3_log_text.see(tk.END)
        self.lab3_log_text.config(state=tk.DISABLED)

    def run_lab3(self, action):
        password = self.password_entry.get()
        filepath = self.lab3_file_path_var.get()

        if not password:
            messagebox.showwarning("Помилка", "Введіть парольну фразу")
            return
        if not filepath:
            messagebox.showwarning("Помилка", "Виберіть файл")
            return

        protector = RC5FileProtector(password)
        filename = os.path.basename(filepath)

        if action == "encrypt":
            out_filepath = filepath + ".enc"
            self.log_lab3(f"Початок шифрування файлу '{filename}'")
            try:
                protector.encrypt_file(filepath, out_filepath)
                self.log_lab3(f"Успіх. Файл збережено як '{os.path.basename(out_filepath)}'\n")
                messagebox.showinfo("Успіх", "Файл успішно зашифровано")
            except Exception as e:
                self.log_lab3(f"Помилка шифрування: {str(e)}\n")

        elif action == "decrypt":
            if filepath.endswith(".enc"):
                out_filepath = filepath[:-4]
            else:
                out_filepath = filepath + "_decrypted"

            self.log_lab3(f"Початок розшифрування файлу '{filename}'")
            try:
                protector.decrypt_file(filepath, out_filepath)
                self.log_lab3(f"Успіх. Файл відновлено як '{os.path.basename(out_filepath)}'\n")
                messagebox.showinfo("Успіх", "Файл успішно розшифровано")
            except Exception as e:
                self.log_lab3(f"Помилка. Можливо, введено неправильний пароль або файл пошкоджено\nДеталі: {str(e)}\n")
                messagebox.showerror("Помилка", "Не вдалося розшифрувати файл. Перевірте пароль")

    def init_lab4_ui(self):
        tk.Label(self.lab4_frame, text="Лабораторна 4: Шифрування RSA", font=("Arial", 14, "bold")).pack(pady=10)

        key_frame = tk.Frame(self.lab4_frame)
        key_frame.pack(pady=10)
        tk.Button(key_frame, text="Згенерувати ключі RSA", command=self.generate_keys_lab4, bg="lightyellow", width=25).pack()

        file_frame = tk.Frame(self.lab4_frame)
        file_frame.pack(pady=15)
        self.lab4_file_path_var = tk.StringVar()
        tk.Button(file_frame, text="Вибрати файл", command=self.select_file_lab4).pack(side=tk.LEFT, padx=5)

        file_entry = tk.Entry(file_frame, textvariable=self.lab4_file_path_var, width=40, state='readonly')
        file_entry.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self.lab4_frame)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Зашифрувати файл", command=lambda: self.run_lab4("encrypt"), bg="lightgreen", width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Розшифрувати файл", command=lambda: self.run_lab4("decrypt"), bg="lightcoral", width=20).pack(side=tk.LEFT, padx=10)

        tk.Button(self.lab4_frame, text="Назад до меню", command=self.show_main_menu).pack(pady=20)

        self.lab4_log_text = tk.Text(self.lab4_frame, height=10, width=75, state=tk.DISABLED)
        self.lab4_log_text.pack(pady=10)

    def show_lab4(self):
        self.main_frame.pack_forget()
        self.lab1_frame.pack_forget()
        self.lab2_frame.pack_forget()
        self.lab3_frame.pack_forget()
        self.lab5_frame.pack_forget()
        self.lab4_frame.pack(fill="both", expand=True)
        self.update_idletasks()

    def select_file_lab4(self):
        filepath = filedialog.askopenfilename(title="Виберіть файл для шифрування/дешифрування RSA")
        if filepath:
            self.lab4_file_path_var.set(filepath)

    def log_lab4(self, message):
        self.lab4_log_text.config(state=tk.NORMAL)
        self.lab4_log_text.insert(tk.END, message + "\n")
        self.lab4_log_text.see(tk.END)
        self.lab4_log_text.config(state=tk.DISABLED)

    def generate_keys_lab4(self):
        protector = RSAFileProtector()
        self.log_lab4("Початок генерації ключів")
        self.update_idletasks()
        try:
            protector.generate_and_save_keys()
            self.log_lab4("Успіх. Ключі private_key.pem та public_key.pem збережено\n")
            messagebox.showinfo("Успіх", "Ключі RSA успішно згенеровано")
        except Exception as e:
            self.log_lab4(f"Помилка генерації ключів: {str(e)}\n")

    def run_lab4(self, action):
        filepath = self.lab4_file_path_var.get()
        if not filepath:
            messagebox.showwarning("Помилка", "Виберіть файл")
            return

        protector = RSAFileProtector()
        filename = os.path.basename(filepath)

        if action == "encrypt":
            out_filepath = filepath + ".rsa"
            self.log_lab4(f"Початок шифрування файлу '{filename}'")
            try:
                protector.encrypt_file(filepath, out_filepath)
                self.log_lab4(f"Успіх. Файл збережено як '{os.path.basename(out_filepath)}'\n")
                messagebox.showinfo("Успіх", "Файл успішно зашифровано (RSA)")
            except Exception as e:
                self.log_lab4(f"Помилка шифрування: {str(e)}\n")
                messagebox.showerror("Помилка", f"Не вдалося зашифрувати:\n{str(e)}")

        elif action == "decrypt":
            if filepath.endswith(".rsa"):
                out_filepath = filepath[:-4]
            else:
                out_filepath = filepath + "_decrypted"

            self.log_lab4(f"Початок розшифрування файлу '{filename}'")
            try:
                protector.decrypt_file(filepath, out_filepath)
                self.log_lab4(f"Успіх. Файл відновлено як '{os.path.basename(out_filepath)}'\n")
                messagebox.showinfo("Успіх", "Файл успішно розшифровано (RSA)")
            except Exception as e:
                self.log_lab4(f"Помилка розшифрування: {str(e)}\n")
                messagebox.showerror("Помилка", "Не вдалося розшифрувати файл. Перевірте наявність приватного ключа")

    def init_lab5_ui(self):
        tk.Label(self.lab5_frame, text="Лабораторна 5: Цифровий підпис (DSS)", font=("Arial", 14, "bold")).pack(pady=10)

        key_frame = tk.Frame(self.lab5_frame)
        key_frame.pack(pady=10)
        tk.Button(key_frame, text="Згенерувати ключі DSA", command=self.generate_keys_lab5, bg="lightyellow", width=25).pack()

        file_frame = tk.Frame(self.lab5_frame)
        file_frame.pack(pady=15)
        self.lab5_file_path_var = tk.StringVar()
        tk.Button(file_frame, text="Вибрати файл", command=self.select_file_lab5).pack(side=tk.LEFT, padx=5)

        file_entry = tk.Entry(file_frame, textvariable=self.lab5_file_path_var, width=40, state='readonly')
        file_entry.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self.lab5_frame)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Підписати файл", command=lambda: self.run_lab5("sign"), bg="lightgreen", width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Перевірити підпис", command=lambda: self.run_lab5("verify"), bg="lightcoral", width=20).pack(side=tk.LEFT, padx=10)

        tk.Button(self.lab5_frame, text="Назад до меню", command=self.show_main_menu).pack(pady=20)

        self.lab5_log_text = tk.Text(self.lab5_frame, height=10, width=75, state=tk.DISABLED)
        self.lab5_log_text.pack(pady=10)

    def show_lab5(self):
        self.main_frame.pack_forget()
        self.lab1_frame.pack_forget()
        self.lab2_frame.pack_forget()
        self.lab3_frame.pack_forget()
        self.lab4_frame.pack_forget()
        self.lab5_frame.pack(fill="both", expand=True)
        self.update_idletasks()

    def select_file_lab5(self):
        filepath = filedialog.askopenfilename(title="Виберіть файл для цифрового підпису DSS")
        if filepath:
            self.lab5_file_path_var.set(filepath)

    def log_lab5(self, message):
        self.lab5_log_text.config(state=tk.NORMAL)
        self.lab5_log_text.insert(tk.END, message + "\n")
        self.lab5_log_text.see(tk.END)
        self.lab5_log_text.config(state=tk.DISABLED)

    def generate_keys_lab5(self):
        protector = DSSProtector()
        self.log_lab5("Початок генерації ключів")
        self.update_idletasks()
        try:
            protector.generate_and_save_keys()
            self.log_lab5("Ключі dsa_private_key.pem та dsa_public_key.pem збережено\n")
            messagebox.showinfo("Успіх", "Ключі DSA успішно згенеровано")
        except Exception as e:
            self.log_lab5(f"Помилка генерації ключів: {str(e)}\n")

    def run_lab5(self, action):
        filepath = self.lab5_file_path_var.get()
        if not filepath:
            messagebox.showwarning("Помилка", "Виберіть файл")
            return

        protector = DSSProtector()
        filename = os.path.basename(filepath)
        sig_filepath = filepath + ".sig"

        if action == "sign":
            self.log_lab5(f"Початок підписування файлу '{filename}'")
            try:
                protector.sign_file(filepath, sig_filepath)
                self.log_lab5(f"Підпис збережено як '{os.path.basename(sig_filepath)}'\n")
                messagebox.showinfo("Успіх", "Файл успішно підписано (DSS)")
            except Exception as e:
                self.log_lab5(f"Помилка підписування: {str(e)}\n")
                messagebox.showerror("Помилка", f"Не вдалося підписати:\n{str(e)}")

        elif action == "verify":
            self.log_lab5(f"Початок перевірки підпису для файлу '{filename}'")
            if not os.path.exists(sig_filepath):
                self.log_lab5("Помилка: Файл підпису (.sig) не знайдено\n")
                messagebox.showerror("Помилка", "Файл підпису (.sig) не знайдено поруч із файлом")
                return
            try:
                is_valid = protector.verify_file(filepath, sig_filepath)
                if is_valid:
                    self.log_lab5("Успіх. Підпис дійсний. Цілісність підтверджено\n")
                    messagebox.showinfo("Успіх", "Цифровий підпис дійсний")
                else:
                    self.log_lab5("Увага. Підпис не дійсний. Файл змінено або підпис підроблено\n")
                    messagebox.showwarning("Увага", "Цифровий підпис НЕ дійсний")
            except Exception as e:
                self.log_lab5(f"Помилка перевірки: {str(e)}\n")
                messagebox.showerror("Помилка", f"Не вдалося перевірити підпис:\n{str(e)}")

if __name__ == "__main__":
    app = InfoSecApp()
    app.mainloop()