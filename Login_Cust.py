import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox

def Login_Cust():
    mn=tk.Tk()
    mn.title("Customer Login")
    mn.geometry("450x450")
    mn.resizable(False,False)
    mn.configure(bg="#2C3E50")

    # Title
    title_label=tk.Label(mn,text="Customer Login",font=("Helvetica",24,"bold"),bg="#2C3E50",fg="#ECF0F1")
    title_label.pack(pady=30)

    # Frame for inputs
    frame=tk.Frame(mn,bg="#34495E",padx=20,pady=20)
    frame.pack(pady=20)

    # Username
    lbl_username=tk.Label(frame,text="Username:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_username.grid(row=0,column=0,sticky="w",pady=10)
    entry_username=tk.Entry(frame,font=("Arial",12),width=25,relief="flat",bd=2)
    entry_username.grid(row=0,column=1,pady=10,padx=10)

    # Password
    lbl_password=tk.Label(frame,text="Password:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_password.grid(row=1,column=0,sticky="w",pady=10)
    entry_password=tk.Entry(frame,font=("Arial",12),width=25,show="*",relief="flat",bd=2)
    entry_password.grid(row=1,column=1,pady=10,padx=10)

    def authenticate_user():
        username=entry_username.get()
        password=entry_password.get()

        if not username or not password:
            messagebox.showerror("Error","Please fill in all fields")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on>"
            )

            cursor=conn.cursor()
            cursor.execute("SELECT Cust_Id FROM Login_Cust WHERE Username=%s AND Password=%s",(username,password))
            result=cursor.fetchone()

            if result:
                cust_id=result[0]
                messagebox.showinfo("Login Successful",f"Welcome,{username}!")
                mn.destroy()
                from Cust_Dash import open_dashboard
                open_dashboard(cust_id)
            else:
                messagebox.showerror("Login Failed","Invalid credentials")

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Login button
    btn_login=tk.Button(mn,text="Login",font=("Arial",14,"bold"),bg="#27AE60",fg="white",
                          activebackground="#229954",relief="flat",width=15,command=authenticate_user)
    btn_login.pack(pady=10)

    # Register button
    def open_register():
        mn.destroy()
        import Cust_Reg
        Cust_Reg.Register_Cust()

    def back():
        if messagebox.askokcancel("Go back","Do You want to return to Main Menu"):
            mn.destroy()
            import Main
            Main.open_main_page()
    btn_register=tk.Button(mn,text="Create New Account",font=("Arial",12),bg="#3498DB",fg="white",
                            activebackground="#2980B9",relief="flat",width=18,command=open_register)
    btn_register.pack(pady=5)

    # Back button
    btn_back=tk.Button(mn,text="← Back",font=("Arial",11),bg="#95A5A6",fg="white",
                        activebackground="#7F8C8D",relief="flat",width=10,command=back)
    btn_back.pack(pady=10)

    mn.mainloop()
