import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox

def Login_Admin():
    mn=tk.Tk()
    mn.title("Admin Login")
    mn.geometry("450x450")
    mn.resizable(False,False)
    mn.configure(bg="#1C2833")

    # Title
    title_label=tk.Label(mn,text="Admin Login",font=("Helvetica",24,"bold"),bg="#1C2833",fg="#F39C12")
    title_label.pack(pady=30)

    # Frame for inputs
    frame=tk.Frame(mn,bg="#273746",padx=20,pady=20)
    frame.pack(pady=20)

    # Username
    lbl_username=tk.Label(frame,text="Admin Username:",font=("Arial",12),bg="#273746",fg="#ECF0F1")
    lbl_username.grid(row=0,column=0,sticky="w",pady=10)
    entry_username=tk.Entry(frame,font=("Arial",12),width=25,relief="flat",bd=2)
    entry_username.grid(row=0,column=1,pady=10,padx=10)

    # Password
    lbl_password=tk.Label(frame,text="Admin Password:",font=("Arial",12),bg="#273746",fg="#ECF0F1")
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
            cursor.execute("SELECT AdminID,Username FROM Login_Admin WHERE Username=%s AND Password=%s",(username,password))
            result=cursor.fetchone()

            if result:
                admin_id=result[0]
                admin_name=result[1]
                messagebox.showinfo("Login Successful",f"Welcome,Admin {admin_name}!")
                mn.destroy()
                from Admin_Dash import open_admin_dashboard
                open_admin_dashboard(admin_id)
            else:
                messagebox.showerror("Login Failed","Invalid credentials")

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Login button
    btn_login=tk.Button(mn,text="Login",font=("Arial",14,"bold"),bg="#E74C3C",fg="white",
                          activebackground="#C0392B",relief="flat",width=15,command=authenticate_user)
    btn_login.pack(pady=10)

    # Register button
    def open_register():
        mn.destroy()
        import Admin_Reg
        Admin_Reg.Register_Admin()
    def go_back():
        if messagebox.askokcancel("Go Back","Returning to Main Page"):
            mn.destroy()
            import Main
            Main.open_main_page()
    btn_register=tk.Button(mn,text="Register New Admin",font=("Arial",12),bg="#F39C12",fg="white",
                            activebackground="#E67E22",relief="flat",width=18,command=open_register)
    btn_register.pack(pady=5)

    # Back button
    btn_back=tk.Button(mn,text="← Back",font=("Arial",11),bg="#95A5A6",fg="white",
                        activebackground="#7F8C8D",relief="flat",width=10,command=go_back)
    btn_back.pack(pady=10)

    mn.mainloop()
