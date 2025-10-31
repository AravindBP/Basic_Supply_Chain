import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk
from datetime import date

def create_navbar(parent,cust_id,active_page):
    """Creates a consistent navbar for all customer pages"""
    navbar=tk.Frame(parent,bg="#1C2833",height=60)
    navbar.pack(side="top",fill="x")
    navbar.pack_propagate(False)
    
    # Page navigation functions
    def go_to_dashboard():
        if active_page != "dashboard":
            parent.destroy()
            from Cust_Dash import open_dashboard
            open_dashboard(cust_id)
    
    def go_to_orders():
        if active_page != "orders":
            parent.destroy()
            from Cust_Orders import open_orders
            open_orders(cust_id)
    
    def go_to_shipments():
        if active_page != "shipments":
            parent.destroy()
            from Cust_Ship import open_shipments
            open_shipments(cust_id)
    
    def go_to_profile():
        if active_page != "profile":
            parent.destroy()
            from Cust_Prof import open_profile
            open_profile(cust_id)
    def logout():
        confirm=messagebox.askyesno("Logout","Are you sure you want to logout?")
        if confirm:
            parent.destroy()
            import Main
            Main.open_main_page()
    # Navbar buttons with active state styling
    btn_dashboard=tk.Button(
        navbar,text="🛒 Products",font=("Arial",11,"bold"),
        bg="#3498DB" if active_page == "dashboard" else "#34495E",
        fg="white",activebackground="#2980B9",relief="flat",
        command=go_to_dashboard,width=12,height=2
    )
    btn_dashboard.pack(side="left",padx=5,pady=10)
    
    btn_orders=tk.Button(
        navbar,text="📦 My Orders",font=("Arial",11,"bold"),
        bg="#27AE60" if active_page == "orders" else "#34495E",
        fg="white",activebackground="#229954",relief="flat",
        command=go_to_orders,width=12,height=2
    )
    btn_orders.pack(side="left",padx=5,pady=10)
    
    btn_shipments=tk.Button(
        navbar,text="🚚 Shipments",font=("Arial",11,"bold"),
        bg="#9B59B6" if active_page == "shipments" else "#34495E",
        fg="white",activebackground="#8E44AD",relief="flat",
        command=go_to_shipments,width=12,height=2
    )
    btn_shipments.pack(side="left",padx=5,pady=10)
    
    btn_profile=tk.Button(
        navbar,text="👤 Profile",font=("Arial",11,"bold"),
        bg="#E67E22" if active_page == "profile" else "#34495E",
        fg="white",activebackground="#D35400",relief="flat",
        command=go_to_profile,width=12,height=2
    )
    btn_profile.pack(side="left",padx=5,pady=10)
    
    btn_logout=tk.Button(
        navbar,text="🚪 Logout",font=("Arial",11,"bold"),
        bg="#E74C3C",fg="white",activebackground="#C0392B",
        relief="flat",command=logout,width=12,height=2
    )
    btn_logout.pack(side="right",padx=10,pady=10)
    
    return navbar


def open_dashboard(cust_id):
    root=tk.Tk()
    root.title("Customer Dashboard")
    root.geometry("1000x650")
    root.resizable(False,False)
    root.configure(bg="#2C3E50")

    # Create navbar
    create_navbar(root,cust_id,"dashboard")

    # ===================== TITLE =====================
    title_label=tk.Label(
        root,
        text="Product Catalog",
        font=("Helvetica",24,"bold"),
        bg="#2C3E50",
        fg="#ECF0F1"
    )
    title_label.pack(pady=20)

    # ===================== SEARCH FRAME =====================
    search_frame=tk.Frame(root,bg="#34495E",padx=10,pady=10)
    search_frame.pack(pady=10,fill="x",padx=20)

    lbl_search=tk.Label(search_frame,text="Search Product:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_search.pack(side="left",padx=5)

    entry_search=tk.Entry(search_frame,font=("Arial",12),width=30)
    entry_search.pack(side="left",padx=5)

    def search_products():
        load_products(entry_search.get())

    btn_search=tk.Button(
        search_frame,text="Search",font=("Arial",11),
        bg="#3498DB",fg="white",activebackground="#2980B9",
        command=search_products,width=10
    )
    btn_search.pack(side="left",padx=5)

    btn_refresh=tk.Button(
        search_frame,text="Refresh",font=("Arial",11),
        bg="#95A5A6",fg="white",activebackground="#7F8C8D",
        command=lambda: load_products(),width=10
    )
    btn_refresh.pack(side="left",padx=5)

    # ===================== PRODUCT TABLE =====================
    table_frame=tk.Frame(root,bg="#2C3E50")
    table_frame.pack(pady=10,fill="both",expand=True,padx=20)

    columns=("Product_ID","Name","Available_Qty","UOM","Unit_Cost")
    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=12)

    tree.heading("Product_ID",text="Product ID")
    tree.heading("Name",text="Product Name")
    tree.heading("Available_Qty",text="Available Quantity")
    tree.heading("UOM",text="Unit of Measure")
    tree.heading("Unit_Cost",text="Unit Cost ($)")

    tree.column("Product_ID",width=120,anchor="center")
    tree.column("Name",width=250,anchor="w")
    tree.column("Available_Qty",width=130,anchor="center")
    tree.column("UOM",width=150,anchor="center")
    tree.column("Unit_Cost",width=130,anchor="center")

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True)

    # ===================== LOAD PRODUCTS =====================
    def load_products(search_term=""):
        for item in tree.get_children():
            tree.delete(item)

        conn=None
        cursor=None

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
                    p.Product_ID,
                    p.Name,
                    COALESCE(SUM(i.Available_QTY),0) AS Available_Qty,
                    p.UOM,
                    p.Unit_Cost
                FROM product p
                LEFT JOIN inventory i ON p.Product_ID=i.Product_ID
            """

            if search_term:
                query += " WHERE p.Name LIKE %s OR p.Product_ID LIKE %s"

            query += " GROUP BY p.Product_ID,p.Name,p.UOM,p.Unit_Cost ORDER BY p.Product_ID"

            if search_term:
                cursor.execute(query,(f"%{search_term}%",f"%{search_term}%"))
            else:
                cursor.execute(query)

            rows=cursor.fetchall()
            for row in rows:
                product_id,name,available_qty,uom,unit_cost=row
                formatted_row=(product_id,name,available_qty,uom,f"${unit_cost:.2f}")
                
                if available_qty == 0:
                    tree.insert("","end",values=formatted_row,tags=('out_of_stock',))
                elif available_qty < 10:
                    tree.insert("","end",values=formatted_row,tags=('low_stock',))
                else:
                    tree.insert("","end",values=formatted_row)

            tree.tag_configure('out_of_stock',background='#E74C3C',foreground='white')
            tree.tag_configure('low_stock',background='#F39C12',foreground='white')

        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ===================== ORDER FRAME =====================
    order_frame=tk.Frame(root,bg="#34495E",padx=20,pady=15)
    order_frame.pack(pady=10,fill="x",padx=20)

    lbl_product=tk.Label(order_frame,text="Product ID:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_product.grid(row=0,column=0,padx=5,pady=5)
    entry_product=tk.Entry(order_frame,font=("Arial",12),width=15)
    entry_product.grid(row=0,column=1,padx=5,pady=5)

    lbl_qty=tk.Label(order_frame,text="Quantity:",font=("Arial",12),bg="#34495E",fg="#ECF0F1")
    lbl_qty.grid(row=0,column=2,padx=5,pady=5)
    entry_qty=tk.Entry(order_frame,font=("Arial",12),width=10)
    entry_qty.grid(row=0,column=3,padx=5,pady=5)

    def place_order():
        product_id=entry_product.get().strip()
        qty=entry_qty.get().strip()

        if not product_id or not qty:
            messagebox.showerror("Error","Please fill in all fields")
            return

        conn=None
        cursor=None

        try:
            qty=int(qty)
            
            if qty <= 0:
                messagebox.showerror("Error","Quantity must be greater than 0")
                return
            
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            # Check stock availability and get unit cost
            cursor.execute("""
                SELECT COALESCE(SUM(i.Available_QTY),0),p.Unit_Cost,p.Name
                FROM product p
                LEFT JOIN inventory i ON p.Product_ID=i.Product_ID
                WHERE p.Product_ID=%s
                GROUP BY p.Product_ID,p.Unit_Cost,p.Name
            """,(product_id,))
            result=cursor.fetchone()

            if not result:
                messagebox.showerror("Error","Product not found")
                return

            available_qty,unit_cost,product_name=result

            if available_qty < qty:
                messagebox.showerror("Error",f"Insufficient stock!\n\nAvailable: {available_qty}\nRequested: {qty}")
                return

            # Calculate total cost
            total_cost=unit_cost * qty
            today=date.today()

            # Generate next Order_ID
            cursor.execute("SELECT MAX(CAST(SUBSTRING(Order_ID,2) AS UNSIGNED)) FROM orders")
            max_id=cursor.fetchone()[0]
            order_id=f"O{((max_id or 0) + 1):03d}"

            # Insert new order
            cursor.execute("""
                INSERT INTO orders (Order_ID,Order_Date,Qty,Status,Cust_ID,Product_ID)
                VALUES (%s,%s,%s,'pending',%s,%s)
            """,(order_id,today,qty,cust_id,product_id))

            # Update inventory
            cursor.execute("""
                UPDATE inventory 
                SET 
                    Available_QTY=Available_QTY - %s,
                    Reserved_QTY=COALESCE(Reserved_QTY,0) + %s
                WHERE Product_ID=%s
            """,(qty,qty,product_id))

            # Generate Shipment_ID
            cursor.execute("SELECT MAX(CAST(SUBSTRING(Shipment_ID,4) AS UNSIGNED)) FROM shipment")
            max_shp_id=cursor.fetchone()[0]
            shipment_id=f"SHP{((max_shp_id or 0) + 1):03d}"

            # Create Shipment record
            cursor.execute("""
                INSERT INTO shipment (Shipment_ID,Order_ID,Shipment_Date,Status)
                VALUES (%s,%s,%s,'Pending')
            """,(shipment_id,order_id,today))

            # Generate Invoice_ID
            cursor.execute("SELECT MAX(CAST(SUBSTRING(Invoice_ID,4) AS UNSIGNED)) FROM invoice")
            max_inv_id=cursor.fetchone()[0]
            invoice_id=f"INV{((max_inv_id or 0) + 1):03d}"

            # Create Invoice record
            cursor.execute("""
                INSERT INTO invoice (Invoice_ID,Order_ID,Total_Amount,Invoice_Date)
                VALUES (%s,%s,%s,%s)
            """,(invoice_id,order_id,total_cost,today))

            conn.commit()
            
            messagebox.showinfo("✅ Order Placed Successfully!",
                               f"Order Details:\n"
                               f"━━━━━━━━━━━━━━━━━━━━━\n"
                               f"Order ID: {order_id}\n"
                               f"Product: {product_name}\n"
                               f"Quantity: {qty}\n"
                               f"Unit Cost: ${unit_cost:.2f}\n"
                               f"Total Cost: ${total_cost:.2f}\n\n"
                               f"Shipment ID: {shipment_id}\n"
                               f"Invoice ID: {invoice_id}\n"
                               f"Date: {today}")

            entry_product.delete(0,tk.END)
            entry_qty.delete(0,tk.END)
            load_products()

        except ValueError:
            messagebox.showerror("Error","Quantity must be a valid number")
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    btn_order=tk.Button(
        order_frame,text="Place Order",font=("Arial",12,"bold"),
        bg="#27AE60",fg="white",activebackground="#229954",
        command=place_order,width=15
    )
    btn_order.grid(row=0,column=4,padx=10,pady=5)

    # Initial load
    load_products()
    root.mainloop()
