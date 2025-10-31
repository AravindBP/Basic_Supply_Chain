import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox

def Register_Admin():
    mn=tk.Tk()
    mn.title("Admin Registration")
    mn.geometry("500x450")
    mn.resizable(False,False)
    mn.configure(bg="#1C2833")

    # Title
    title_label=tk.Label(mn,text="Admin Registration",font=("Helvetica",24,"bold"),bg="#1C2833",fg="#F39C12")
    title_label.pack(pady=30)

    # Info Label
    info_label=tk.Label(mn,text="Admin registration requires authorization",
                         font=("Arial",11,"italic"),bg="#1C2833",fg="#E67E22")
    info_label.pack(pady=5)

    # Frame for inputs
    frame=tk.Frame(mn,bg="#273746",padx=20,pady=20)
    frame.pack(pady=20)

    # Username
    lbl_username=tk.Label(frame,text="Admin Username:",font=("Arial",12),bg="#273746",fg="#ECF0F1")
    lbl_username.grid(row=0,column=0,sticky="w",pady=10)
    entry_username=tk.Entry(frame,font=("Arial",12),width=25,relief="flat",bd=2)
    entry_username.grid(row=0,column=1,pady=10,padx=10)

    # Password
    lbl_password=tk.Label(frame,text="Password:",font=("Arial",12),bg="#273746",fg="#ECF0F1")
    lbl_password.grid(row=1,column=0,sticky="w",pady=10)
    entry_password=tk.Entry(frame,font=("Arial",12),width=25,show="*",relief="flat",bd=2)
    entry_password.grid(row=1,column=1,pady=10,padx=10)

    # Confirm Password
    lbl_confirm=tk.Label(frame,text="Confirm Password:",font=("Arial",12),bg="#273746",fg="#ECF0F1")
    lbl_confirm.grid(row=2,column=0,sticky="w",pady=10)
    entry_confirm=tk.Entry(frame,font=("Arial",12),width=25,show="*",relief="flat",bd=2)
    entry_confirm.grid(row=2,column=1,pady=10,padx=10)

    # Admin Secret Key
    lbl_secret=tk.Label(frame,text="Admin Secret Key:",font=("Arial",12),bg="#273746",fg="#ECF0F1")
    lbl_secret.grid(row=3,column=0,sticky="w",pady=10)
    entry_secret=tk.Entry(frame,font=("Arial",12),width=25,show="*",relief="flat",bd=2)
    entry_secret.grid(row=3,column=1,pady=10,padx=10)

    def register_admin():
        username=entry_username.get().strip()
        password=entry_password.get().strip()
        confirm=entry_confirm.get().strip()
        secret_key=entry_secret.get().strip()

        # Validation
        if not all([username,password,confirm,secret_key]):
            messagebox.showerror("Error","Please fill in all fields")
            return

        # Check secret key (you can change this to any secure key)
        ADMIN_SECRET_KEY="ADMIN2025"  # Change this to your secure key
        if secret_key != ADMIN_SECRET_KEY:
            messagebox.showerror("Error","Invalid Admin Secret Key")
            return

        if password != confirm:
            messagebox.showerror("Error","Passwords do not match")
            return

        if len(password) < 6:
            messagebox.showerror("Error","Password must be at least 6 characters")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password>",
                database="<Database_Name>"
            )
            cursor=conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM Login_Admin WHERE Username=%s",(username,))
            if cursor.fetchone():
                messagebox.showerror("Error","Username already exists")
                cursor.close()
                conn.close()
                return

            # Insert into Login_Admin table
            cursor.execute("""
                INSERT INTO Login_Admin (Username,Password)
                VALUES (%s,%s)
            """,(username,password))

            conn.commit()
            admin_id=cursor.lastrowid
            messagebox.showinfo("Success",f"Admin registration successful! Your Admin ID is: {admin_id}")
            
            cursor.close()
            conn.close()
            
            mn.destroy()
            import Login_Admin
            Login_Admin.Login_Admin()

        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Register button
    btn_register=tk.Button(mn,text="Register",font=("Arial",14,"bold"),bg="#E74C3C",fg="white",
                            activebackground="#C0392B",relief="flat",width=15,command=register_admin)
    btn_register.pack(pady=15)

    # Back to Login button
    def back_to_login():
        mn.destroy()
        import Login_Admin
        Login_Admin.Login_Admin()

    btn_back=tk.Button(mn,text="← Back to Login",font=("Arial",11),bg="#95A5A6",fg="white",
                        activebackground="#7F8C8D",relief="flat",width=15,command=back_to_login)
    btn_back.pack(pady=5)

    mn.mainloop()
