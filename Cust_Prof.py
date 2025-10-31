import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox
from Cust_Dash import create_navbar

def open_profile(cust_id):
    root=tk.Tk()
    root.title("My Profile")
    root.geometry("600x550")
    root.resizable(False,False)
    root.configure(bg="#2C3E50")

    # Create navbar
    create_navbar(root,cust_id,"profile")

    # Title
    title_label=tk.Label(root,text="My Profile",font=("Helvetica",24,"bold"),bg="#2C3E50",fg="#ECF0F1")
    title_label.pack(pady=30)

    # Profile Frame
    frame=tk.Frame(root,bg="#34495E",padx=30,pady=20)
    frame.pack(pady=20)

    # Labels and Entries
    lbl_name=tk.Label(frame,text="Full Name:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_name.grid(row=0,column=0,sticky="w",pady=10)
    entry_name=tk.Entry(frame,font=("Arial",12),width=25)
    entry_name.grid(row=0,column=1,pady=10,padx=10)

    lbl_phone=tk.Label(frame,text="Phone Number:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_phone.grid(row=1,column=0,sticky="w",pady=10)
    entry_phone=tk.Entry(frame,font=("Arial",12),width=25)
    entry_phone.grid(row=1,column=1,pady=10,padx=10)

    lbl_address=tk.Label(frame,text="Address:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_address.grid(row=2,column=0,sticky="w",pady=10)
    entry_address=tk.Entry(frame,font=("Arial",12),width=25)
    entry_address.grid(row=2,column=1,pady=10,padx=10)

    lbl_email=tk.Label(frame,text="Email:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_email.grid(row=3,column=0,sticky="w",pady=10)
    entry_email=tk.Entry(frame,font=("Arial",12),width=25,state="readonly")
    entry_email.grid(row=3,column=1,pady=10,padx=10)

    # Load customer data
    def load_profile():
        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on> "
            )
            cursor=conn.cursor()
            cursor.execute("SELECT Full_Name,Phone_No,Address,Mail FROM customer WHERE Cust_Id=%s",(cust_id,))
            result=cursor.fetchone()

            if result:
                entry_name.insert(0,result[0])
                entry_phone.insert(0,result[1])
                entry_address.insert(0,result[2])
                entry_email.config(state="normal")
                entry_email.insert(0,result[3])
                entry_email.config(state="readonly")

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    def update_profile():
        name=entry_name.get()
        phone=entry_phone.get()
        address=entry_address.get()

        if not name or not phone or not address:
            messagebox.showerror("Error","Please fill in all fields")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on> "
            )
            cursor=conn.cursor()
            cursor.execute("""
                UPDATE customer 
                SET Full_Name=%s,Phone_No=%s,Address=%s
                WHERE Cust_Id=%s
            """,(name,phone,address,cust_id))
            
            conn.commit()
            messagebox.showinfo("Success","Profile updated successfully!")

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Buttons
    btn_update=tk.Button(root,text="Update Profile",font=("Arial",13,"bold"),bg="#27AE60",fg="white",
                           activebackground="#229954",command=update_profile,width=15)
    btn_update.pack(pady=10)

    load_profile()
    root.mainloop()
