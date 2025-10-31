import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk


def open_manage_products(admin_id):
    root=tk.Tk()
    root.title("Product Management")
    root.geometry("1200x750")
    root.resizable(False,False)
    root.configure(bg="#1C2833")

    # Create navbar with admin_id
    from Admin_Dash import create_admin_navbar
    create_admin_navbar(root,admin_id,"products")

    # Title
    title_label=tk.Label(root,text="Product Management",font=("Helvetica",20,"bold"),
                          bg="#1C2833",fg="#9B59B6")
    title_label.pack(pady=12)

    # Search Frame
    search_frame=tk.Frame(root,bg="#273746",padx=15,pady=10)
    search_frame.pack(pady=8,fill="x",padx=20)

    lbl_search=tk.Label(search_frame,text="Search Product:",font=("Arial",11),
                         bg="#273746",fg="#ECF0F1")
    lbl_search.pack(side="left",padx=8)

    entry_search=tk.Entry(search_frame,font=("Arial",11),width=25)
    entry_search.pack(side="left",padx=5)

    def search_products():
        load_products(entry_search.get())

    btn_search=tk.Button(search_frame,text="🔍 Search",font=("Arial",10,"bold"),
                          bg="#3498DB",fg="white",command=search_products,width=10)
    btn_search.pack(side="left",padx=5)

    btn_refresh=tk.Button(search_frame,text="🔄 Refresh",font=("Arial",10,"bold"),
                           bg="#95A5A6",fg="white",command=lambda: load_products(),width=10)
    btn_refresh.pack(side="left",padx=5)

    # Back to Inventory Button
    def back_to_inventory():
        root.destroy()
        import Admin_Inv
        Admin_Inv.open_admin_inventory(admin_id)

    btn_back=tk.Button(search_frame,text="← Back to Inventory",font=("Arial",10,"bold"),
                        bg="#34495E",fg="white",command=back_to_inventory,width=18)
    btn_back.pack(side="left",padx=5)

    # Products Table
    table_frame=tk.Frame(root,bg="#1C2833")
    table_frame.pack(pady=8,fill="both",expand=False,padx=20)

    columns=("Product_ID","Name","UOM","Reorder_Point","Reorder_Qty")
    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=10)

    tree.heading("Product_ID",text="Product ID")
    tree.heading("Name",text="Product Name")
    tree.heading("UOM",text="Unit of Measure")
    tree.heading("Reorder_Point",text="Reorder Point")
    tree.heading("Reorder_Qty",text="Reorder Quantity")

    tree.column("Product_ID",width=120,anchor="center")
    tree.column("Name",width=250,anchor="w")
    tree.column("UOM",width=150,anchor="center")
    tree.column("Reorder_Point",width=120,anchor="center")
    tree.column("Reorder_Qty",width=150,anchor="center")

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True)

    def load_products(search_term=""):
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password>",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            query="SELECT Product_ID,Name,UOM,Reorder_Point,Reorder_Qty FROM product"

            if search_term:
                query += " WHERE Name LIKE %s OR Product_ID LIKE %s"
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

    # Operations Container
    operations_frame=tk.Frame(root,bg="#1C2833")
    operations_frame.pack(pady=10,fill="both",expand=True,padx=20)

    # Left Column: Add Product
    left_column=tk.Frame(operations_frame,bg="#1C2833")
    left_column.pack(side="left",fill="both",expand=True,padx=(0,10))

    # Add Product Frame
    add_frame=tk.Frame(left_column,bg="#273746",padx=20,pady=15)
    add_frame.pack(fill="both",expand=True)

    tk.Label(add_frame,text="Add New Product",
             font=("Arial",12,"bold"),bg="#273746",fg="#27AE60").grid(row=0,column=0,columnspan=2,pady=(0,15))

    tk.Label(add_frame,text="Product ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=1,column=0,padx=8,pady=8,sticky="e")
    entry_product_id=tk.Entry(add_frame,font=("Arial",10),width=20)
    entry_product_id.grid(row=1,column=1,padx=8,pady=8)

    tk.Label(add_frame,text="Product Name:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=2,column=0,padx=8,pady=8,sticky="e")
    entry_name=tk.Entry(add_frame,font=("Arial",10),width=20)
    entry_name.grid(row=2,column=1,padx=8,pady=8)

    tk.Label(add_frame,text="Unit of Measure:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=3,column=0,padx=8,pady=8,sticky="e")
    entry_uom=tk.Entry(add_frame,font=("Arial",10),width=20)
    entry_uom.grid(row=3,column=1,padx=8,pady=8)

    tk.Label(add_frame,text="Reorder Point:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=4,column=0,padx=8,pady=8,sticky="e")
    entry_reorder_point=tk.Entry(add_frame,font=("Arial",10),width=20)
    entry_reorder_point.grid(row=4,column=1,padx=8,pady=8)

    tk.Label(add_frame,text="Reorder Quantity:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=5,column=0,padx=8,pady=8,sticky="e")
    entry_reorder_qty=tk.Entry(add_frame,font=("Arial",10),width=20)
    entry_reorder_qty.grid(row=5,column=1,padx=8,pady=8)

    def add_product():
        product_id=entry_product_id.get().strip()
        name=entry_name.get().strip()
        uom=entry_uom.get().strip()
        reorder_point=entry_reorder_point.get().strip()
        reorder_qty=entry_reorder_qty.get().strip()

        if not all([product_id,name,uom,reorder_point,reorder_qty]):
            messagebox.showerror("Error","Please fill in all fields")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password>",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            cursor.execute("""
                INSERT INTO product (Product_ID,Name,UOM,Reorder_Point,Reorder_Qty)
                VALUES (%s,%s,%s,%s,%s)
            """,(product_id,name,uom,int(reorder_point),int(reorder_qty)))

            conn.commit()
            messagebox.showinfo("Success",f"Product Added\n\nProduct ID: {product_id}\nName:{name}")
            
            entry_product_id.delete(0,tk.END)
            entry_name.delete(0,tk.END)
            entry_uom.delete(0,tk.END)
            entry_reorder_point.delete(0,tk.END)
            entry_reorder_qty.delete(0,tk.END)
            
            load_products()

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")
        except ValueError:
            messagebox.showerror("Error","Numeric fields must contain valid numbers")

    # Add Product Button - Properly visible
    btn_add=tk.Button(add_frame,text="➕ Add Product",font=("Arial",11,"bold"),
                       bg="#27AE60",fg="white",command=add_product,width=25,height=2)
    btn_add.grid(row=6,column=0,columnspan=2,pady=20,padx=20,sticky="ew")

    # Right Column: Delete Product
    right_column=tk.Frame(operations_frame,bg="#1C2833")
    right_column.pack(side="right",fill="both",expand=True,padx=(10,0))

    # Delete Product Frame
    delete_frame=tk.Frame(right_column,bg="#273746",padx=20,pady=15)
    delete_frame.pack(fill="both",expand=True)

    tk.Label(delete_frame,text="🗑️ Delete Product",
             font=("Arial",12,"bold"),bg="#273746",fg="#E74C3C").pack(pady=(0,15))

    warning_label=tk.Label(delete_frame,
                            text="WARNING: Cannot delete products that are referenced\n"
                                 "in other tables (inventory,orders,etc.)\n"
                                 "Delete associated records first!",
                            font=("Arial",9,"italic"),bg="#273746",fg="#F39C12",
                            wraplength=350,justify="center")
    warning_label.pack(pady=(0,20))

    input_frame_del=tk.Frame(delete_frame,bg="#273746")
    input_frame_del.pack(pady=10)

    tk.Label(input_frame_del,text="Product ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=0,column=0,padx=8,pady=8,sticky="e")
    entry_delete_product_id=tk.Entry(input_frame_del,font=("Arial",10),width=20)
    entry_delete_product_id.grid(row=0,column=1,padx=8,pady=8)

    def delete_product():
        product_id=entry_delete_product_id.get().strip()
        if not product_id:
            messagebox.showerror("Error","Please enter Product ID")
            return

        confirm=messagebox.askyesno("Confirm Delete",
                                      f"Delete product '{product_id}'?\n\nThis action cannot be undone!")
        if not confirm:
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password>",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            # Check if product exists
            cursor.execute("SELECT Product_ID,Name FROM product WHERE Product_ID=%s",(product_id,))
            result=cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error",f"Product ID '{product_id}' not found")
                cursor.close()
                conn.close()
                return

            prod_id,product_name=result

            # Try to delete - will fail if foreign key constraint violated
            cursor.execute("DELETE FROM product WHERE Product_ID=%s",(product_id,))
            
            conn.commit()
            
            messagebox.showinfo("Success",
                               f"Product Deleted!\n\n"
                               f"Product ID: {prod_id}\n"
                               f"Name: {product_name}")
            entry_delete_product_id.delete(0,tk.END)
            load_products()

            cursor.close()
            conn.close()
        except mysql.IntegrityError as e:
            messagebox.showerror("Cannot Delete",
                               f"Cannot delete product '{product_id}'!\n\n"
                               f"Reason: This product is referenced in other tables\n"
                               f"(inventory,orders,shipments,etc.)\n\n"
                               f"Please delete all associated records first.")
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_delete=tk.Button(delete_frame,text="Delete Product",font=("Arial",11,"bold"),
                          bg="#E74C3C",fg="white",command=delete_product,width=20,height=2)
    btn_delete.pack(pady=15)

    load_products()
    root.mainloop()
