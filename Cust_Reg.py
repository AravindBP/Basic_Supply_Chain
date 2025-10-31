import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox

def Register_Cust():
    mn=tk.Tk()
    mn.title("Customer Registration")
    mn.geometry("500x650")
    mn.resizable(False,False)
    mn.configure(bg="#2C3E50")

    # Title
    title_label=tk.Label(mn,text="Customer Registration",font=("Helvetica",24,"bold"),bg="#2C3E50",fg="#ECF0F1")
    title_label.pack(pady=20)

    # Frame for inputs
    frame=tk.Frame(mn,bg="#34495E",padx=20,pady=20)
    frame.pack(pady=10)

    # Full Name
    lbl_fullname=tk.Label(frame,text="Full Name:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_fullname.grid(row=0,column=0,sticky="w",pady=10)
    entry_fullname=tk.Entry(frame,font=("Arial",12),width=30,relief="flat",bd=2)
    entry_fullname.grid(row=0,column=1,pady=10,padx=10)

    # Phone Number
    lbl_phone=tk.Label(frame,text="Phone Number:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_phone.grid(row=1,column=0,sticky="w",pady=10)
    entry_phone=tk.Entry(frame,font=("Arial",12),width=30,relief="flat",bd=2)
    entry_phone.grid(row=1,column=1,pady=10,padx=10)

    # Address
    lbl_address=tk.Label(frame,text="Address:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_address.grid(row=2,column=0,sticky="w",pady=10)
    entry_address=tk.Entry(frame,font=("Arial",12),width=30,relief="flat",bd=2)
    entry_address.grid(row=2,column=1,pady=10,padx=10)

    # Email
    lbl_mail=tk.Label(frame,text="Email:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_mail.grid(row=3,column=0,sticky="w",pady=10)
    entry_mail=tk.Entry(frame,font=("Arial",12),width=30,relief="flat",bd=2)
    entry_mail.grid(row=3,column=1,pady=10,padx=10)

    # Username
    lbl_username=tk.Label(frame,text="Username:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_username.grid(row=4,column=0,sticky="w",pady=10)
    entry_username=tk.Entry(frame,font=("Arial",12),width=30,relief="flat",bd=2)
    entry_username.grid(row=4,column=1,pady=10,padx=10)

    # Password
    lbl_password=tk.Label(frame,text="Password:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_password.grid(row=5,column=0,sticky="w",pady=10)
    entry_password=tk.Entry(frame,font=("Arial",12),width=30,show="*",relief="flat",bd=2)
    entry_password.grid(row=5,column=1,pady=10,padx=10)

    # Confirm Password
    lbl_confirm=tk.Label(frame,text="Confirm Password:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_confirm.grid(row=6,column=0,sticky="w",pady=10)
    entry_confirm=tk.Entry(frame,font=("Arial",12),width=30,show="*",relief="flat",bd=2)
    entry_confirm.grid(row=6,column=1,pady=10,padx=10)

    def register_customer():
        fullname=entry_fullname.get().strip()
        phone=entry_phone.get().strip()
        address=entry_address.get().strip()
        mail=entry_mail.get().strip()
        username=entry_username.get().strip()
        password=entry_password.get().strip()
        confirm=entry_confirm.get().strip()

        # Validation
        if not all([fullname,phone,address,mail,username,password,confirm]):
            messagebox.showerror("Error","Please fill in all fields")
            return

        if password != confirm:
            messagebox.showerror("Error","Passwords do not match")
            return

        if len(password) < 6:
            messagebox.showerror("Error","Password must be at least 6 characters")
            return

        try:
            phone_int=int(phone)
            if len(phone) != 10:
                messagebox.showerror("Error","Phone number must be 10 digits")
                return
        except ValueError:
            messagebox.showerror("Error","Phone number must be numeric")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on>"
            )
            cursor=conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM Login_Cust WHERE Username=%s",(username,))
            if cursor.fetchone():
                messagebox.showerror("Error","Username already exists")
                cursor.close()
                conn.close()
                return

            # Insert into customer table
            cursor.execute("""
                INSERT INTO customer (Full_Name,Phone_No,Address,Mail)
                VALUES (%s,%s,%s,%s)
            """,(fullname,phone_int,address,mail))

            # Get the auto-generated Cust_Id
            cust_id=cursor.lastrowid

            # Insert into Login_Cust table
            cursor.execute("""
                INSERT INTO Login_Cust (Cust_Id,Username,Password)
                VALUES (%s,%s,%s)
            """,(cust_id,username,password))

            conn.commit()
            messagebox.showinfo("Success",f"Registration successful! Your Customer ID is: {cust_id}\n\nPlease login to continue.")
            
            cursor.close()
            conn.close()
            
            mn.destroy()
            import Login_Cust
            Login_Cust.Login_Cust()

        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Register button
    btn_register=tk.Button(mn,text="Register",font=("Arial",14,"bold"),bg="#27AE60",fg="white",
                            activebackground="#229954",relief="flat",width=15,command=register_customer)
    btn_register.pack(pady=10)

    # Divider
    divider_frame=tk.Frame(mn,bg="#2C3E50")
    divider_frame.pack(pady=5)
    
    tk.Label(divider_frame,text="Already have an account?",
            font=("Arial",10),bg="#2C3E50",fg="#95A5A6").pack()

    # Sign In button
    def go_to_login():
        mn.destroy()
        import Login_Cust
        Login_Cust.Login_Cust()

    btn_signin=tk.Button(mn,text="Sign In",font=("Arial",12,"bold"),bg="#3498DB",fg="white",
                          activebackground="#2980B9",relief="flat",width=15,command=go_to_login)
    btn_signin.pack(pady=5)

    # Back button
    btn_back=tk.Button(mn,text="← Back to Main",font=("Arial",10),bg="#95A5A6",fg="white",
                        activebackground="#7F8C8D",relief="flat",width=12,command=mn.destroy)
    btn_back.pack(pady=10)

    mn.mainloop()
