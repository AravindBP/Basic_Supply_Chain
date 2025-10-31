import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk
from Admin_Dash import create_admin_navbar


def open_admin_suppliers(admin_id):
    root=tk.Tk()
    root.title("Supplier Management")
    root.geometry("1100x700")
    root.resizable(False,False)
    root.configure(bg="#1C2833")

    # Create navbar with admin_id
    create_admin_navbar(root,admin_id,"suppliers")

    # Title
    title_label=tk.Label(root,text="Supplier Management",font=("Helvetica",24,"bold"),
                          bg="#1C2833",fg="#F39C12")
    title_label.pack(pady=20)

    # Search Frame
    search_frame=tk.Frame(root,bg="#273746",padx=10,pady=10)
    search_frame.pack(pady=10,fill="x",padx=20)

    lbl_search=tk.Label(search_frame,text="Search Supplier:",font=("Arial",11),
                         bg="#273746",fg="#ECF0F1")
    lbl_search.pack(side="left",padx=5)

    entry_search=tk.Entry(search_frame,font=("Arial",11),width=25)
    entry_search.pack(side="left",padx=5)

    def search_suppliers():
        load_suppliers(entry_search.get())

    btn_search=tk.Button(search_frame,text="Search",font=("Arial",10),
                          bg="#3498DB",fg="white",command=search_suppliers,width=10)
    btn_search.pack(side="left",padx=5)

    btn_refresh=tk.Button(search_frame,text="Refresh",font=("Arial",10),
                           bg="#95A5A6",fg="white",command=lambda: load_suppliers(),width=10)
    btn_refresh.pack(side="left",padx=5)

    # Suppliers Table
    table_frame=tk.Frame(root,bg="#1C2833")
    table_frame.pack(pady=10,fill="both",expand=True,padx=20)

    columns=("Supplier_ID","Name","Mail","Contact_No","Address","Rating")
    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=10)

    for col in columns:
        tree.heading(col,text=col)
        tree.column(col,width=170,anchor="center")

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True)

    def load_suppliers(search_term=""):
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            query="SELECT Supplier_ID,Name,Mail,Contact_No,Address,Rating FROM supplier"

            if search_term:
                query += " WHERE Name LIKE %s OR Supplier_ID LIKE %s"
                cursor.execute(query,(f"%{search_term}%",f"%{search_term}%"))
            else:
                cursor.execute(query)

            rows=cursor.fetchall()
            for row in rows:
                tree.insert("","end",values=row)

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Add/Update Supplier Frame
    form_frame=tk.Frame(root,bg="#273746",padx=20,pady=15)
    form_frame.pack(pady=10,fill="x",padx=20)

    # Row 1
    lbl_id=tk.Label(form_frame,text="Supplier ID:",font=("Arial",10),bg="#273746",fg="#ECF0F1")
    lbl_id.grid(row=0,column=0,padx=5,pady=5,sticky="w")
    entry_id=tk.Entry(form_frame,font=("Arial",10),width=12)
    entry_id.grid(row=0,column=1,padx=5,pady=5)

    lbl_name=tk.Label(form_frame,text="Name:",font=("Arial",10),bg="#273746",fg="#ECF0F1")
    lbl_name.grid(row=0,column=2,padx=5,pady=5,sticky="w")
    entry_name=tk.Entry(form_frame,font=("Arial",10),width=20)
    entry_name.grid(row=0,column=3,padx=5,pady=5)

    lbl_mail=tk.Label(form_frame,text="Email:",font=("Arial",10),bg="#273746",fg="#ECF0F1")
    lbl_mail.grid(row=0,column=4,padx=5,pady=5,sticky="w")
    entry_mail=tk.Entry(form_frame,font=("Arial",10),width=20)
    entry_mail.grid(row=0,column=5,padx=5,pady=5)

    # Row 2
    lbl_contact=tk.Label(form_frame,text="Contact:",font=("Arial",10),bg="#273746",fg="#ECF0F1")
    lbl_contact.grid(row=1,column=0,padx=5,pady=5,sticky="w")
    entry_contact=tk.Entry(form_frame,font=("Arial",10),width=12)
    entry_contact.grid(row=1,column=1,padx=5,pady=5)

    lbl_address=tk.Label(form_frame,text="Address:",font=("Arial",10),bg="#273746",fg="#ECF0F1")
    lbl_address.grid(row=1,column=2,padx=5,pady=5,sticky="w")
    entry_address=tk.Entry(form_frame,font=("Arial",10),width=30)
    entry_address.grid(row=1,column=3,columnspan=2,padx=5,pady=5)

    lbl_rating=tk.Label(form_frame,text="Rating:",font=("Arial",10),bg="#273746",fg="#ECF0F1")
    lbl_rating.grid(row=1,column=5,padx=5,pady=5,sticky="w")
    entry_rating=tk.Entry(form_frame,font=("Arial",10),width=8)
    entry_rating.grid(row=1,column=6,padx=5,pady=5)

    def add_supplier():
        supplier_id=entry_id.get().strip()
        name=entry_name.get().strip()
        mail=entry_mail.get().strip()
        contact=entry_contact.get().strip()
        address=entry_address.get().strip()
        rating=entry_rating.get().strip()

        if not all([supplier_id,name,mail,contact,address]):
            messagebox.showerror("Error","Please fill in all required fields")
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
                INSERT INTO supplier (Supplier_ID,Name,Mail,Contact_No,Address,Rating)
                VALUES (%s,%s,%s,%s,%s,%s)
            """,(supplier_id,name,mail,int(contact),address,float(rating) if rating else None))

            conn.commit()
            messagebox.showinfo("Success",f"Supplier {supplier_id} added successfully!")
            
            # Clear entries
            for entry in [entry_id,entry_name,entry_mail,entry_contact,entry_address,entry_rating]:
                entry.delete(0,tk.END)
            
            load_suppliers()

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    def update_supplier():
        supplier_id=entry_id.get().strip()
        name=entry_name.get().strip()
        mail=entry_mail.get().strip()
        contact=entry_contact.get().strip()
        address=entry_address.get().strip()
        rating=entry_rating.get().strip()

        if not supplier_id:
            messagebox.showerror("Error","Please enter Supplier ID")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            updates=[]
            params=[]

            if name:
                updates.append("Name=%s")
                params.append(name)
            if mail:
                updates.append("Mail=%s")
                params.append(mail)
            if contact:
                updates.append("Contact_No=%s")
                params.append(int(contact))
            if address:
                updates.append("Address=%s")
                params.append(address)
            if rating:
                updates.append("Rating=%s")
                params.append(float(rating))

            if not updates:
                messagebox.showerror("Error","No fields to update")
                return

            params.append(supplier_id)
            query=f"UPDATE supplier SET {','.join(updates)} WHERE Supplier_ID=%s"

            cursor.execute(query,params)

            if cursor.rowcount == 0:
                messagebox.showerror("Error","Supplier not found")
            else:
                conn.commit()
                messagebox.showinfo("Success",f"Supplier {supplier_id} updated!")
                load_suppliers()

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    def delete_supplier():
        supplier_id=entry_id.get().strip()

        if not supplier_id:
            messagebox.showerror("Error","Please enter Supplier ID")
            return

        confirm=messagebox.askyesno("Confirm",f"Delete supplier {supplier_id}?")
        if not confirm:
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            cursor.execute("DELETE FROM supplier WHERE Supplier_ID=%s",(supplier_id,))

            if cursor.rowcount == 0:
                messagebox.showerror("Error","Supplier not found")
            else:
                conn.commit()
                messagebox.showinfo("Success",f"Supplier {supplier_id} deleted!")
                load_suppliers()

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Buttons
    btn_frame=tk.Frame(root,bg="#1C2833")
    btn_frame.pack(pady=10)

    btn_add=tk.Button(btn_frame,text="Add Supplier",font=("Arial",11,"bold"),
                       bg="#27AE60",fg="white",command=add_supplier,width=15)
    btn_add.pack(side="left",padx=5)

    btn_update=tk.Button(btn_frame,text="Update Supplier",font=("Arial",11,"bold"),
                          bg="#3498DB",fg="white",command=update_supplier,width=15)
    btn_update.pack(side="left",padx=5)

    btn_delete=tk.Button(btn_frame,text="Delete Supplier",font=("Arial",11,"bold"),
                          bg="#E74C3C",fg="white",command=delete_supplier,width=15)
    btn_delete.pack(side="left",padx=5)

    load_suppliers()
    root.mainloop()
