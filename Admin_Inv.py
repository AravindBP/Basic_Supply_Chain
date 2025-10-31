import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk


def open_admin_inventory(admin_id):
    root=tk.Tk()
    root.title("Inventory Management")
    root.geometry("1300x850")
    root.resizable(False,False)
    root.configure(bg="#1C2833")

    # Create navbar with admin_id
    from Admin_Dash import create_admin_navbar
    create_admin_navbar(root,admin_id,"inventory")

    # Title
    title_label=tk.Label(root,text="Inventory Management",font=("Helvetica",20,"bold"),
                          bg="#1C2833",fg="#F39C12")
    title_label.pack(pady=12)

    # Search and Filter Frame
    filter_frame=tk.Frame(root,bg="#273746",padx=15,pady=10)
    filter_frame.pack(pady=8,fill="x",padx=20)

    lbl_search=tk.Label(filter_frame,text="Search Product:",font=("Arial",11),
                         bg="#273746",fg="#ECF0F1")
    lbl_search.pack(side="left",padx=8)

    entry_search=tk.Entry(filter_frame,font=("Arial",11),width=25)
    entry_search.pack(side="left",padx=5)

    def search_inventory():
        load_inventory(entry_search.get())

    btn_search=tk.Button(filter_frame,text="🔍 Search",font=("Arial",10,"bold"),
                          bg="#3498DB",fg="white",command=search_inventory,width=10)
    btn_search.pack(side="left",padx=5)

    btn_refresh=tk.Button(filter_frame,text="🔄 Refresh",font=("Arial",10,"bold"),
                           bg="#95A5A6",fg="white",command=lambda: load_inventory(),width=10)
    btn_refresh.pack(side="left",padx=5)

    # Inventory Table
    table_frame=tk.Frame(root,bg="#1C2833")
    table_frame.pack(pady=8,fill="both",expand=False,padx=20)

    columns=("Inventory_ID","Product_ID","Product_Name","Available_Qty","Reserved_Qty",
               "In_Transit_Qty","Warehouse_ID","Reorder_Point","Reorder_Qty")
    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=8)

    tree.heading("Inventory_ID",text="Inv ID")
    tree.heading("Product_ID",text="Product ID")
    tree.heading("Product_Name",text="Product Name")
    tree.heading("Available_Qty",text="Available")
    tree.heading("Reserved_Qty",text="Reserved")
    tree.heading("In_Transit_Qty",text="In Transit")
    tree.heading("Warehouse_ID",text="Warehouse")
    tree.heading("Reorder_Point",text="Reorder Pt")
    tree.heading("Reorder_Qty",text="Reorder Qty")

    tree.column("Inventory_ID",width=75,anchor="center")
    tree.column("Product_ID",width=95,anchor="center")
    tree.column("Product_Name",width=160,anchor="w")
    tree.column("Available_Qty",width=80,anchor="center")
    tree.column("Reserved_Qty",width=80,anchor="center")
    tree.column("In_Transit_Qty",width=80,anchor="center")
    tree.column("Warehouse_ID",width=90,anchor="center")
    tree.column("Reorder_Point",width=90,anchor="center")
    tree.column("Reorder_Qty",width=95,anchor="center")

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True)

    def load_inventory(search_term=""):
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<password>",
                database="<Database to work on>"
            )
            cursor=conn.cursor()

            query="SELECT * FROM Inv_Prod"

            if search_term:
                query += " WHERE Name LIKE %s OR Product_ID LIKE %s"
                cursor.execute(query,(f"%{search_term}%",f"%{search_term}%"))
            else:
                cursor.execute(query)

            rows=cursor.fetchall()
            for row in rows:
                available_qty=row[3] if row[3] is not None else 0
                reorder_point=row[7] if row[7] is not None else 0
                
                if available_qty < reorder_point:
                    tree.insert("","end",values=row,tags=('low_stock',))
                else:
                    tree.insert("","end",values=row)

            tree.tag_configure('low_stock',background='#E74C3C',foreground='white')

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Operations Container
    operations_frame=tk.Frame(root,bg="#1C2833")
    operations_frame.pack(pady=8,fill="both",expand=True,padx=20)

    # Left Column: Add & Delete Inventory
    left_column=tk.Frame(operations_frame,bg="#1C2833")
    left_column.pack(side="left",fill="both",expand=True,padx=(0,10))

    # Add Inventory Frame
    add_frame=tk.Frame(left_column,bg="#273746",padx=18,pady=15)
    add_frame.pack(fill="x",pady=(0,10))

    tk.Label(add_frame,text="➕ Add Inventory Record",
             font=("Arial",12,"bold"),bg="#273746",fg="#F39C12").grid(row=0,column=0,columnspan=4,pady=(0,10))

    tk.Label(add_frame,text="Inventory ID:",font=("Arial",10),bg="#273746",fg="#ECF0F1").grid(row=1,column=0,padx=5,pady=5,sticky="e")
    entry_inventory_id=tk.Entry(add_frame,font=("Arial",10),width=12)
    entry_inventory_id.grid(row=1,column=1,padx=5,pady=5)

    tk.Label(add_frame,text="Product ID:",font=("Arial",10),bg="#273746",fg="#ECF0F1").grid(row=1,column=2,padx=5,pady=5,sticky="e")
    entry_product_id=tk.Entry(add_frame,font=("Arial",10),width=12)
    entry_product_id.grid(row=1,column=3,padx=5,pady=5)

    tk.Label(add_frame,text="Available Qty:",font=("Arial",10),bg="#273746",fg="#ECF0F1").grid(row=2,column=0,padx=5,pady=5,sticky="e")
    entry_available_qty=tk.Entry(add_frame,font=("Arial",10),width=12)
    entry_available_qty.insert(0,"0")
    entry_available_qty.grid(row=2,column=1,padx=5,pady=5)

    tk.Label(add_frame,text="Reserved Qty:",font=("Arial",10),bg="#273746",fg="#ECF0F1").grid(row=2,column=2,padx=5,pady=5,sticky="e")
    entry_reserved_qty=tk.Entry(add_frame,font=("Arial",10),width=12)
    entry_reserved_qty.insert(0,"0")
    entry_reserved_qty.grid(row=2,column=3,padx=5,pady=5)

    tk.Label(add_frame,text="In Transit Qty:",font=("Arial",10),bg="#273746",fg="#ECF0F1").grid(row=3,column=0,padx=5,pady=5,sticky="e")
    entry_in_transit_qty=tk.Entry(add_frame,font=("Arial",10),width=12)
    entry_in_transit_qty.insert(0,"0")
    entry_in_transit_qty.grid(row=3,column=1,padx=5,pady=5)

    tk.Label(add_frame,text="Warehouse:",font=("Arial",10),bg="#273746",fg="#ECF0F1").grid(row=3,column=2,padx=5,pady=5,sticky="e")
    entry_warehouse=tk.Entry(add_frame,font=("Arial",10),width=12)
    entry_warehouse.insert(0,"W001")
    entry_warehouse.grid(row=3,column=3,padx=5,pady=5)

    def add_inventory():
        # ...existing code...
        pass

    def auto_generate_inv_id():
        # ...existing code...
        pass

    btn_frame=tk.Frame(add_frame,bg="#273746")
    btn_frame.grid(row=4,column=0,columnspan=4,pady=10)

    btn_auto_id=tk.Button(btn_frame,text="Auto-Generate ID",font=("Arial",10,"bold"),
                           bg="#3498DB",fg="white",command=auto_generate_inv_id,width=18)
    btn_auto_id.pack(side="left",padx=5)

    btn_add=tk.Button(btn_frame,text="➕ Add Inventory",font=("Arial",10,"bold"),
                       bg="#27AE60",fg="white",command=add_inventory,width=18)
    btn_add.pack(side="left",padx=5)

    # Delete Inventory Frame
    delete_inv_frame=tk.Frame(left_column,bg="#273746",padx=18,pady=15)
    delete_inv_frame.pack(fill="x")

    # ...existing delete code...

    # Right Column: Update Stock
    right_column=tk.Frame(operations_frame,bg="#1C2833")
    right_column.pack(side="right",fill="both",expand=True,padx=(10,0))

    # Update Stock Frame
    update_frame=tk.Frame(right_column,bg="#273746",padx=18,pady=15)
    update_frame.pack(fill="both",expand=True)

    tk.Label(update_frame,text="📦 Update Stock Quantity",
             font=("Arial",12,"bold"),bg="#273746",fg="#3498DB").pack(pady=(0,15))

    input_frame=tk.Frame(update_frame,bg="#273746")
    input_frame.pack(pady=10)

    tk.Label(input_frame,text="Product ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=0,column=0,padx=8,pady=8,sticky="e")
    entry_product_id_upd=tk.Entry(input_frame,font=("Arial",10),width=18)
    entry_product_id_upd.grid(row=0,column=1,padx=8,pady=8)

    tk.Label(input_frame,text="New Quantity:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=1,column=0,padx=8,pady=8,sticky="e")
    entry_qty=tk.Entry(input_frame,font=("Arial",10),width=18)
    entry_qty.grid(row=1,column=1,padx=8,pady=8)

    def update_stock():
        product_id=entry_product_id_upd.get().strip()
        new_qty=entry_qty.get().strip()

        if not product_id or not new_qty:
            messagebox.showerror("Error","Please fill in all fields")
            return

        try:
            new_qty=int(new_qty)
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<password>",
                database="<Database to work on>"
            )
            cursor=conn.cursor()

            # Get current stock and reorder info
            cursor.execute("""
                SELECT i.Available_QTY,p.Reorder_Point,p.Reorder_Qty 
                FROM inventory i
                JOIN product p ON i.Product_ID=p.Product_ID
                WHERE i.Product_ID=%s
            """,(product_id,))
            result=cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error","Product not found in inventory")
                cursor.close()
                conn.close()
                return

            old_qty=result[0] if result[0] is not None else 0
            reorder_point=result[1] if result[1] is not None else 0
            reorder_qty=result[2] if result[2] is not None else 0

            # Determine if trigger will activate
            will_trigger=new_qty < reorder_point
            expected_final_qty=(new_qty + reorder_qty) if will_trigger else new_qty

            # Update the quantity - BEFORE trigger will modify it if needed
            cursor.execute("""
                UPDATE inventory 
                SET Available_QTY=%s
                WHERE Product_ID=%s
            """,(new_qty,product_id))

            conn.commit()

            # Get the actual final quantity after trigger
            cursor.execute("SELECT Available_QTY FROM inventory WHERE Product_ID=%s",(product_id,))
            final_qty=cursor.fetchone()[0]

            # Check if trigger was activated
            if final_qty != new_qty:
                messagebox.showinfo("Auto-Reorder Triggered!",
                                   f"Auto-Reorder System Activated!\n\n"
                                   f"Old Quantity: {old_qty}\n"
                                   f"You set: {new_qty}\n"
                                   f"Reorder Point: {reorder_point}\n\n"
                                   f"System Auto-Added: {reorder_qty} units\n"
                                   f"Final Quantity: {final_qty}")
            else:
                messagebox.showinfo("Success",
                                   f"Stock Updated!\n\n"
                                   f"Old Quantity: {old_qty}\n"
                                   f"New Quantity: {final_qty}\n\n"
                                   f"Reorder Point: {reorder_point}")

            entry_product_id_upd.delete(0,tk.END)
            entry_qty.delete(0,tk.END)
            load_inventory()

            cursor.close()
            conn.close()
        except ValueError:
            messagebox.showerror("Error","Quantity must be a valid number")
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_update=tk.Button(update_frame,text="📦 Update Stock",font=("Arial",11,"bold"),
                          bg="#3498DB",fg="white",command=update_stock,width=20,height=2)
    btn_update.pack(pady=15)

    load_inventory()
    root.mainloop()
