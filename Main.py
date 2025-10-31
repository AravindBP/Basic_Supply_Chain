import tkinter as tk
from tkinter import messagebox

def open_main_page():
    root=tk.Tk()
    root.title("Supply Chain Management System")
    root.geometry("600x550")
    root.resizable(False,False)
    root.configure(bg="#2C3E50")

    # Title
    title_label=tk.Label(root,text="Supply Chain DBMS",
                          font=("Helvetica",32,"bold"),
                          bg="#2C3E50",fg="#ECF0F1")
    title_label.pack(pady=30)

    subtitle_label=tk.Label(root,text="Welcome! Please select your role:",
                             font=("Arial",16),
                             bg="#2C3E50",fg="#95A5A6")
    subtitle_label.pack(pady=20)

    # Role Selection Frame
    role_frame=tk.Frame(root,bg="#2C3E50")
    role_frame.pack(pady=30)

    # Customer Login Button
    def open_customer_login():
        root.destroy()
        import Login_Cust
        Login_Cust.Login_Cust()

    btn_customer=tk.Button(role_frame,text="👤 Customer Login",
                            font=("Arial",18,"bold"),
                            bg="#3498DB",fg="white",
                            activebackground="#2980B9",
                            relief="raised",
                            bd=3,
                            command=open_customer_login,
                            width=20,height=3)
    btn_customer.pack(pady=15)

    # Admin Login Button
    def open_admin_login():
        root.destroy()
        import Login_Admin
        Login_Admin.Login_Admin()

    btn_admin=tk.Button(role_frame,text="🔐 Admin Login",
                         font=("Arial",18,"bold"),
                         bg="#E74C3C",fg="white",
                         activebackground="#C0392B",
                         relief="raised",
                         bd=3,
                         command=open_admin_login,
                         width=20,height=3)
    btn_admin.pack(pady=15)

    # Exit Button
    btn_exit=tk.Button(root,text="Exit Application",
                        font=("Arial",13,"bold"),
                        bg="#7F8C8D",fg="white",
                        activebackground="#5D6D7E",
                        relief="flat",
                        command=root.destroy,
                        width=15)
    btn_exit.pack(pady=20)

    # Footer
    footer_label=tk.Label(root,text="Supply Chain Management System",
                           font=("Arial",10),
                           bg="#2C3E50",fg="#7F8C8D")
    footer_label.pack(side="bottom",pady=10)

    root.mainloop()

open_main_page()