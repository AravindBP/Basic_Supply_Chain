import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk
from Admin_Dash import create_admin_navbar


def open_admin_prod_sup(admin_id):
    root=tk.Tk()
    root.title("Product-Supplier Management")
    root.geometry("1300x800")
    root.resizable(False,False)
    root.configure(bg="#1C2833")

    # Create navbar with admin_id
    create_admin_navbar(root,admin_id,"prod_sup")

    # Title
    title_label=tk.Label(root,text="Product-Supplier Relationships",font=("Helvetica",20,"bold"),
                          bg="#1C2833",fg="#E67E22")
    title_label.pack(pady=12)

    # Search and Filter Frame
    filter_frame=tk.Frame(root,bg="#273746",padx=15,pady=10)
    filter_frame.pack(pady=8,fill="x",padx=20)

    lbl_search=tk.Label(filter_frame,text="Search:",font=("Arial",11),
                         bg="#273746",fg="#ECF0F1")
    lbl_search.pack(side="left",padx=8)

    entry_search=tk.Entry(filter_frame,font=("Arial",11),width=20)
    entry_search.pack(side="left",padx=5)

    def search_relationships():
        load_relationships(entry_search.get(),filter_var.get())

    btn_search=tk.Button(filter_frame,text="🔍 Search",font=("Arial",10,"bold"),
                          bg="#3498DB",fg="white",command=search_relationships,width=10)
    btn_search.pack(side="left",padx=5)

    # Filter by Preferrable
    tk.Label(filter_frame,text="Filter:",font=("Arial",11),
            bg="#273746",fg="#ECF0F1").pack(side="left",padx=(20,5))

    filter_var=tk.StringVar(value="All")
    combo_filter=ttk.Combobox(filter_frame,textvariable=filter_var,
                                values=["All","yes","no"],
                                font=("Arial",10),state="readonly",width=10)
    combo_filter.pack(side="left",padx=5)

    def apply_filter():
        load_relationships(entry_search.get(),filter_var.get())

    btn_filter=tk.Button(filter_frame,text="Apply Filter",font=("Arial",10,"bold"),
                          bg="#9B59B6",fg="white",command=apply_filter,width=12)
    btn_filter.pack(side="left",padx=5)

    btn_refresh=tk.Button(filter_frame,text="🔄 Refresh",font=("Arial",10,"bold"),
                           bg="#95A5A6",fg="white",command=lambda: load_relationships(),width=10)
    btn_refresh.pack(side="left",padx=5)

    # Product-Supplier Table
    table_frame=tk.Frame(root,bg="#1C2833")
    table_frame.pack(pady=8,fill="both",expand=False,padx=20)

    columns=("Product_ID","Product_Name","Supplier_ID","Supplier_Name",
               "Lead_Time_days","Preferrable")
    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=10)

    tree.heading("Product_ID",text="Product ID")
    tree.heading("Product_Name",text="Product Name")
    tree.heading("Supplier_ID",text="Supplier ID")
    tree.heading("Supplier_Name",text="Supplier Name")
    tree.heading("Lead_Time_days",text="Lead Time (days)")
    tree.heading("Preferrable",text="Preferred")

    tree.column("Product_ID",width=100,anchor="center")
    tree.column("Product_Name",width=200,anchor="w")
    tree.column("Supplier_ID",width=100,anchor="center")
    tree.column("Supplier_Name",width=200,anchor="w")
    tree.column("Lead_Time_days",width=130,anchor="center")
    tree.column("Preferrable",width=100,anchor="center")

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True)

    def load_relationships(search_term="",filter_pref="All"):
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

            query="""
                SELECT 
                    ps.Product_ID,
                    p.Name AS Product_Name,
                    ps.Supplier_ID,
                    s.Name AS Supplier_Name,
                    ps.Lead_Time_days,
                    ps.Preferrable
                FROM prod_sup ps
                JOIN product p ON ps.Product_ID=p.Product_ID
                JOIN supplier s ON ps.Supplier_ID=s.Supplier_ID
                WHERE 1=1
            """

            params=[]

            if search_term:
                query += " AND (ps.Product_ID LIKE %s OR p.Name LIKE %s OR ps.Supplier_ID LIKE %s OR s.Name LIKE %s)"
                params.extend([f"%{search_term}%",f"%{search_term}%",f"%{search_term}%",f"%{search_term}%"])

            if filter_pref != "All":
                query += " AND LOWER(ps.Preferrable)=%s"
                params.append(filter_pref.lower())

            query += " ORDER BY ps.Product_ID,ps.Preferrable DESC"

            cursor.execute(query,params) if params else cursor.execute(query)

            rows=cursor.fetchall()
            for row in rows:
                preferrable=row[5].lower() if row[5] else "no"
                
                if preferrable == "yes":
                    tree.insert("","end",values=row,tags=('preferred',))
                else:
                    tree.insert("","end",values=row)

            # Configure tag colors
            tree.tag_configure('preferred',background='#27AE60',foreground='white')

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Operations Container
    operations_frame=tk.Frame(root,bg="#1C2833")
    operations_frame.pack(pady=8,fill="both",expand=True,padx=20)

    # Left Column: Add Relationship
    left_column=tk.Frame(operations_frame,bg="#1C2833")
    left_column.pack(side="left",fill="both",expand=True,padx=(0,10))

    add_frame=tk.Frame(left_column,bg="#273746",padx=18,pady=15)
    add_frame.pack(fill="both",expand=True)

    tk.Label(add_frame,text="➕ Add Product-Supplier Relationship",
             font=("Arial",12,"bold"),bg="#273746",fg="#27AE60").pack(pady=(0,15))

    input_frame=tk.Frame(add_frame,bg="#273746")
    input_frame.pack(pady=10)

    tk.Label(input_frame,text="Product ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=0,column=0,padx=8,pady=8,sticky="e")
    entry_product_id=tk.Entry(input_frame,font=("Arial",10),width=18)
    entry_product_id.grid(row=0,column=1,padx=8,pady=8)

    tk.Label(input_frame,text="Supplier ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=1,column=0,padx=8,pady=8,sticky="e")
    entry_supplier_id=tk.Entry(input_frame,font=("Arial",10),width=18)
    entry_supplier_id.grid(row=1,column=1,padx=8,pady=8)

    tk.Label(input_frame,text="Lead Time (days):",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=2,column=0,padx=8,pady=8,sticky="e")
    entry_lead_time=tk.Entry(input_frame,font=("Arial",10),width=18)
    entry_lead_time.grid(row=2,column=1,padx=8,pady=8)

    tk.Label(input_frame,text="Preferred:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=3,column=0,padx=8,pady=8,sticky="e")
    
    pref_var=tk.StringVar(value="no")
    combo_pref=ttk.Combobox(input_frame,textvariable=pref_var,
                              values=["yes","no"],
                              font=("Arial",10),state="readonly",width=16)
    combo_pref.grid(row=3,column=1,padx=8,pady=8)

    def add_relationship():
        product_id=entry_product_id.get().strip()
        supplier_id=entry_supplier_id.get().strip()
        lead_time=entry_lead_time.get().strip()
        preferrable=pref_var.get()

        if not all([product_id,supplier_id,lead_time]):
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

            # Check if product exists
            cursor.execute("SELECT Name FROM product WHERE Product_ID=%s",(product_id,))
            product=cursor.fetchone()
            if not product:
                messagebox.showerror("Error",f"Product ID '{product_id}' does not exist!")
                cursor.close()
                conn.close()
                return

            # Check if supplier exists
            cursor.execute("SELECT Name FROM supplier WHERE Supplier_ID=%s",(supplier_id,))
            supplier=cursor.fetchone()
            if not supplier:
                messagebox.showerror("Error",f"Supplier ID '{supplier_id}' does not exist!")
                cursor.close()
                conn.close()
                return

            # Insert relationship
            cursor.execute("""
                INSERT INTO prod_sup (Product_ID,Supplier_ID,Lead_Time_days,Preferrable)
                VALUES (%s,%s,%s,%s)
            """,(product_id,supplier_id,int(lead_time),preferrable))

            conn.commit()
            messagebox.showinfo("Success",
                               f"Relationship Added!\n\n"
                               f"Product: {product[0]}\n"
                               f"Supplier: {supplier[0]}\n"
                               f"Lead Time: {lead_time} days\n"
                               f"Preferred: {preferrable}")
            
            entry_product_id.delete(0,tk.END)
            entry_supplier_id.delete(0,tk.END)
            entry_lead_time.delete(0,tk.END)
            load_relationships()

            cursor.close()
            conn.close()
        except mysql.IntegrityError:
            messagebox.showerror("Error","This relationship already exists!")
        except ValueError:
            messagebox.showerror("Error","Lead time must be a valid number")
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_add=tk.Button(add_frame,text="➕ Add Relationship",font=("Arial",11,"bold"),
                       bg="#27AE60",fg="white",command=add_relationship,width=20,height=2)
    btn_add.pack(pady=15)

    # Middle Column: Update Relationship
    middle_column=tk.Frame(operations_frame,bg="#1C2833")
    middle_column.pack(side="left",fill="both",expand=True,padx=(0,10))

    update_frame=tk.Frame(middle_column,bg="#273746",padx=18,pady=15)
    update_frame.pack(fill="both",expand=True)

    tk.Label(update_frame,text="📝 Update Relationship",
             font=("Arial",12,"bold"),bg="#273746",fg="#3498DB").pack(pady=(0,15))

    input_frame_upd=tk.Frame(update_frame,bg="#273746")
    input_frame_upd.pack(pady=10)

    tk.Label(input_frame_upd,text="Product ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=0,column=0,padx=8,pady=8,sticky="e")
    entry_upd_product=tk.Entry(input_frame_upd,font=("Arial",10),width=18)
    entry_upd_product.grid(row=0,column=1,padx=8,pady=8)

    tk.Label(input_frame_upd,text="Supplier ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=1,column=0,padx=8,pady=8,sticky="e")
    entry_upd_supplier=tk.Entry(input_frame_upd,font=("Arial",10),width=18)
    entry_upd_supplier.grid(row=1,column=1,padx=8,pady=8)

    tk.Label(input_frame_upd,text="New Lead Time:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=2,column=0,padx=8,pady=8,sticky="e")
    entry_upd_lead=tk.Entry(input_frame_upd,font=("Arial",10),width=18)
    entry_upd_lead.grid(row=2,column=1,padx=8,pady=8)

    tk.Label(input_frame_upd,text="New Preferred:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=3,column=0,padx=8,pady=8,sticky="e")
    
    upd_pref_var=tk.StringVar(value="no")
    combo_upd_pref=ttk.Combobox(input_frame_upd,textvariable=upd_pref_var,
                                  values=["yes","no"],
                                  font=("Arial",10),state="readonly",width=16)
    combo_upd_pref.grid(row=3,column=1,padx=8,pady=8)

    def update_relationship():
        product_id=entry_upd_product.get().strip()
        supplier_id=entry_upd_supplier.get().strip()
        lead_time=entry_upd_lead.get().strip()
        preferrable=upd_pref_var.get()

        if not product_id or not supplier_id:
            messagebox.showerror("Error","Please enter Product ID and Supplier ID")
            return

        if not lead_time:
            messagebox.showerror("Error","Please enter new Lead Time")
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
                UPDATE prod_sup 
                SET Lead_Time_days=%s,Preferrable=%s
                WHERE Product_ID=%s AND Supplier_ID=%s
            """,(int(lead_time),preferrable,product_id,supplier_id))

            if cursor.rowcount == 0:
                messagebox.showerror("Error","Relationship not found")
            else:
                conn.commit()
                messagebox.showinfo("Success",
                                   f"Relationship Updated!\n\n"
                                   f"Product ID: {product_id}\n"
                                   f"Supplier ID: {supplier_id}\n"
                                   f"New Lead Time: {lead_time} days\n"
                                   f"Preferred: {preferrable}")
                
                entry_upd_product.delete(0,tk.END)
                entry_upd_supplier.delete(0,tk.END)
                entry_upd_lead.delete(0,tk.END)
                load_relationships()

            cursor.close()
            conn.close()
        except ValueError:
            messagebox.showerror("Error","Lead time must be a valid number")
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_update=tk.Button(update_frame,text="📝 Update",font=("Arial",11,"bold"),
                          bg="#3498DB",fg="white",command=update_relationship,width=20,height=2)
    btn_update.pack(pady=15)

    # Right Column: Delete Relationship
    right_column=tk.Frame(operations_frame,bg="#1C2833")
    right_column.pack(side="right",fill="both",expand=True)

    delete_frame=tk.Frame(right_column,bg="#273746",padx=18,pady=15)
    delete_frame.pack(fill="both",expand=True)

    tk.Label(delete_frame,text="🗑️ Delete Relationship",
             font=("Arial",12,"bold"),bg="#273746",fg="#E74C3C").pack(pady=(0,15))

    input_frame_del=tk.Frame(delete_frame,bg="#273746")
    input_frame_del.pack(pady=10)

    tk.Label(input_frame_del,text="Product ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=0,column=0,padx=8,pady=8,sticky="e")
    entry_del_product=tk.Entry(input_frame_del,font=("Arial",10),width=18)
    entry_del_product.grid(row=0,column=1,padx=8,pady=8)

    tk.Label(input_frame_del,text="Supplier ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=1,column=0,padx=8,pady=8,sticky="e")
    entry_del_supplier=tk.Entry(input_frame_del,font=("Arial",10),width=18)
    entry_del_supplier.grid(row=1,column=1,padx=8,pady=8)

    def delete_relationship():
        product_id=entry_del_product.get().strip()
        supplier_id=entry_del_supplier.get().strip()

        if not product_id or not supplier_id:
            messagebox.showerror("Error","Please enter both IDs")
            return

        confirm=messagebox.askyesno("Confirm Delete",
                                      f"Delete relationship?\n\n"
                                      f"Product ID: {product_id}\n"
                                      f"Supplier ID: {supplier_id}\n\n"
                                      f"This action cannot be undone!")
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

            cursor.execute("""
                DELETE FROM prod_sup 
                WHERE Product_ID=%s AND Supplier_ID=%s
            """,(product_id,supplier_id))

            if cursor.rowcount == 0:
                messagebox.showerror("Error","Relationship not found")
            else:
                conn.commit()
                messagebox.showinfo("Success",
                                   f"Relationship Deleted!\n\n"
                                   f"Product ID: {product_id}\n"
                                   f"Supplier ID: {supplier_id}")
                
                entry_del_product.delete(0,tk.END)
                entry_del_supplier.delete(0,tk.END)
                load_relationships()

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_delete=tk.Button(delete_frame,text="🗑️ Delete",font=("Arial",11,"bold"),
                          bg="#E74C3C",fg="white",command=delete_relationship,width=20,height=2)
    btn_delete.pack(pady=15)

    load_relationships()
    root.mainloop()
