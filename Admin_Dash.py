import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk

def create_admin_navbar(root,admin_id,active_page="dashboard"):
    """Creates a navbar for admin pages"""
    navbar=tk.Frame(root,bg="#2C3E50",height=60)
    navbar.pack(side="top",fill="x")
    navbar.pack_propagate(False)

    def open_dashboard():
        if active_page!="dashboard":
            root.destroy()
            open_admin_dashboard(admin_id)

    def open_inventory():
        if active_page!="inventory":
            root.destroy()
            from Admin_Inv import open_admin_inventory
            open_admin_inventory(admin_id)

    def open_products():
        if active_page!="products":
            root.destroy()
            from Admin_Prod import open_manage_products
            open_manage_products(admin_id)

    def open_orders():
        if active_page!="orders":
            root.destroy()
            from Admin_Ord import open_admin_orders
            open_admin_orders(admin_id)

    def open_suppliers():
        if active_page!="suppliers":
            root.destroy()
            from Admin_Sup import open_admin_suppliers
            open_admin_suppliers(admin_id)

    def open_prod_sup():
        if active_page!="prod_sup":
            root.destroy()
            from Admin_PS import open_admin_prod_sup
            open_admin_prod_sup(admin_id)

    def logout():
        if messagebox.askyesno("Logout Confirmation","Are you sure you want to logout?"):
            root.destroy()
            import Main
            Main.open_main_page()

    # Navbar buttons
    btn_dashboard=tk.Button(
        navbar,text="🏠 Dashboard",font=("Arial",11,"bold"),
        bg="#3498DB" if active_page == "dashboard" else "#34495E",
        fg="white",activebackground="#2980B9",relief="flat",
        command=open_dashboard,width=12,height=2
    )
    btn_dashboard.pack(side="left",padx=5,pady=10)

    btn_inventory=tk.Button(
        navbar,text="📦 Inventory",font=("Arial",11,"bold"),
        bg="#27AE60" if active_page == "inventory" else "#34495E",
        fg="white",activebackground="#229954",relief="flat",
        command=open_inventory,width=12,height=2
    )
    btn_inventory.pack(side="left",padx=5,pady=10)

    btn_products=tk.Button(
        navbar,text="🛒 Products",font=("Arial",11,"bold"),
        bg="#9B59B6" if active_page == "products" else "#34495E",
        fg="white",activebackground="#8E44AD",relief="flat",
        command=open_products,width=12,height=2
    )
    btn_products.pack(side="left",padx=5,pady=10)

    btn_orders=tk.Button(
        navbar,text="📋 Orders",font=("Arial",11,"bold"),
        bg="#3498DB" if active_page == "orders" else "#34495E",
        fg="white",activebackground="#2980B9",relief="flat",
        command=open_orders,width=12,height=2
    )
    btn_orders.pack(side="left",padx=5,pady=10)

    btn_suppliers=tk.Button(
        navbar,text="🏭 Suppliers",font=("Arial",11,"bold"),
        bg="#F39C12" if active_page == "suppliers" else "#34495E",
        fg="white",activebackground="#E67E22",relief="flat",
        command=open_suppliers,width=12,height=2
    )
    btn_suppliers.pack(side="left",padx=5,pady=10)

    btn_prod_sup=tk.Button(
        navbar,text="🔗 Prod-Supplier",font=("Arial",11,"bold"),
        bg="#E67E22" if active_page == "prod_sup" else "#34495E",
        fg="white",activebackground="#D35400",relief="flat",
        command=open_prod_sup,width=14,height=2
    )
    btn_prod_sup.pack(side="left",padx=5,pady=10)

    # Admin info label
    try:
        conn=mysql.connect(
            host="localhost",
            user="root",
            password="<password>",
            database="dbms"
        )
        cursor=conn.cursor()
        cursor.execute("SELECT Username FROM Login_Admin WHERE Admin_Id=%s",(admin_id,))
        result=cursor.fetchone()
        admin_name=result[0] if result else "Admin"
        cursor.close()
        conn.close()
    except:
        admin_name="Admin"

    lbl_admin=tk.Label(
        navbar,text=f"👤 Admin: {admin_name}",font=("Arial",10,"bold"),
        bg="#2C3E50",fg="#ECF0F1"
    )
    lbl_admin.pack(side="right",padx=20,pady=10)

    btn_logout=tk.Button(
        navbar,text="🚪 Logout",font=("Arial",11,"bold"),
        bg="#E74C3C",fg="white",activebackground="#C0392B",
        relief="flat",command=logout,width=10,height=2
    )
    btn_logout.pack(side="right",padx=10,pady=10)

    return navbar


def open_admin_dashboard(admin_id):
    root=tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("1400x900")
    root.resizable(False,False)
    root.configure(bg="#1C2833")

    # Create navbar
    create_admin_navbar(root,admin_id,"dashboard")

    # Title
    title_label=tk.Label(root,text="Admin Dashboard",font=("Helvetica",24,"bold"),
                          bg="#1C2833",fg="#3498DB")
    title_label.pack(pady=10)

    # Fetch statistics
    try:
        conn=mysql.connect(
            host="localhost",
            user="root",
            password="<Password>",
            database="<Database to operate in>"
        )
        cursor=conn.cursor()

        # Total Products
        cursor.execute("SELECT COUNT(*) FROM product")
        total_products=cursor.fetchone()[0]

        # Total Orders
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders=cursor.fetchone()[0]

        # Pending Orders
        cursor.execute("SELECT COUNT(*) FROM orders WHERE LOWER(Status)='pending'")
        pending_orders=cursor.fetchone()[0]

        # Total Suppliers
        cursor.execute("SELECT COUNT(*) FROM supplier")
        total_suppliers=cursor.fetchone()[0]

        # Total Customers
        cursor.execute("SELECT COUNT(*) FROM customer")
        total_customers=cursor.fetchone()[0]

        # Stock Level Categories
        cursor.execute("""
            SELECT COUNT(DISTINCT i.Product_ID) 
            FROM inventory i 
            WHERE i.Available_QTY < 10
        """)
        critical_stock=cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT i.Product_ID) 
            FROM inventory i 
            WHERE i.Available_QTY >= 10 AND i.Available_QTY < 20
        """)
        low_stock=cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT i.Product_ID) 
            FROM inventory i 
            WHERE i.Available_QTY >= 20
        """)
        normal_stock=cursor.fetchone()[0]

        cursor.close()
        conn.close()
    except mysql.Error as e:
        messagebox.showerror("Database Error",f"Error: {e}")
        total_products=total_orders=pending_orders=total_suppliers=total_customers=0
        critical_stock=low_stock=normal_stock=0

    # TOP SECTION: Summary Cards (2 rows)
    cards_container=tk.Frame(root,bg="#1C2833")
    cards_container.pack(pady=10,padx=40,fill="x")

    # Row 1 - Main Stats
    row1=tk.Frame(cards_container,bg="#1C2833")
    row1.pack(pady=5,fill="x")

    cards_row1=[
        ("📦 Total Products",total_products,"#3498DB"),
        ("📋 Total Orders",total_orders,"#27AE60"),
        ("⏳ Pending Orders",pending_orders,"#F39C12"),
        ("🏭 Suppliers",total_suppliers,"#9B59B6"),
        ("👥 Customers",total_customers,"#E67E22"),
    ]

    for label,value,color in cards_row1:
        card=tk.Frame(row1,bg=color,padx=20,pady=15,relief="raised",bd=2)
        card.pack(side="left",padx=8,expand=True,fill="both")
        tk.Label(card,text=label,font=("Arial",10,"bold"),
                 bg=color,fg="white").pack()
        tk.Label(card,text=str(value),font=("Arial",20,"bold"),
                 bg=color,fg="white").pack()

    # Row 2 - Stock Level Stats
    row2=tk.Frame(cards_container,bg="#1C2833")
    row2.pack(pady=5,fill="x")

    cards_row2=[
        ("✅ Normal Stock",normal_stock,"#27AE60"),
        ("⚠️ Low Stock",low_stock,"#F39C12"),
        ("🚨 Critical Stock",critical_stock,"#E74C3C"),
    ]

    for label,value,color in cards_row2:
        card=tk.Frame(row2,bg=color,padx=20,pady=15,relief="raised",bd=2)
        card.pack(side="left",padx=8,expand=True,fill="both")
        tk.Label(card,text=label,font=("Arial",10,"bold"),
                 bg=color,fg="white").pack()
        tk.Label(card,text=str(value),font=("Arial",20,"bold"),
                 bg=color,fg="white").pack()

    # Spacer cards to maintain layout
    for _ in range(2):
        spacer=tk.Frame(row2,bg="#1C2833")
        spacer.pack(side="left",padx=8,expand=True,fill="both")

    # BOTTOM SECTION: Stock Level Table with Filter
    table_container=tk.Frame(root,bg="#1C2833")
    table_container.pack(pady=10,padx=40,fill="both",expand=True)

    # Title for Stock Table
    stock_title=tk.Label(table_container,text="📊 Product Stock Levels",
                          font=("Arial",16,"bold"),bg="#1C2833",fg="#ECF0F1")
    stock_title.pack(pady=(0,8))

    # Filter Frame
    filter_frame=tk.Frame(table_container,bg="#273746",padx=15,pady=10)
    filter_frame.pack(pady=5,fill="x")

    tk.Label(filter_frame,text="Filter by Stock Level:",font=("Arial",11,"bold"),
             bg="#273746",fg="#ECF0F1").pack(side="left",padx=5)

    filter_var=tk.StringVar(value="All")
    combo_filter=ttk.Combobox(filter_frame,textvariable=filter_var,
                                values=["All","Normal (≥20)","Low (10-19)","Critical (<10)"],
                                font=("Arial",10),state="readonly",width=15)
    combo_filter.pack(side="left",padx=5)

    def apply_filter():
        load_stock_table(filter_var.get())

    btn_filter=tk.Button(filter_frame,text="Apply Filter",font=("Arial",10,"bold"),
                          bg="#3498DB",fg="white",command=apply_filter,width=12)
    btn_filter.pack(side="left",padx=5)

    btn_refresh=tk.Button(filter_frame,text="🔄 Refresh",font=("Arial",10,"bold"),
                           bg="#95A5A6",fg="white",command=lambda: load_stock_table(),width=10)
    btn_refresh.pack(side="left",padx=5)

    # Stock Table
    table_frame=tk.Frame(table_container,bg="#1C2833")
    table_frame.pack(pady=5,fill="both",expand=True)

    columns=("Product_ID","Product_Name","Available_QTY","Reserved_QTY","Status")
    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=12)

    tree.heading("Product_ID",text="Product ID")
    tree.heading("Product_Name",text="Product Name")
    tree.heading("Available_QTY",text="Available")
    tree.heading("Reserved_QTY",text="Reserved")
    tree.heading("Status",text="Stock Status")

    tree.column("Product_ID",width=120,anchor="center")
    tree.column("Product_Name",width=300,anchor="w")
    tree.column("Available_QTY",width=120,anchor="center")
    tree.column("Reserved_QTY",width=120,anchor="center")
    tree.column("Status",width=150,anchor="center")

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True)

    def load_stock_table(filter_level="All"):
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<password>",
                database="dbms"
            )
            cursor=conn.cursor()

            query="""
                SELECT 
                    i.Product_ID,
                    p.Name,
                    i.Available_QTY,
                    i.Reserved_QTY,
                    CASE 
                        WHEN i.Available_QTY >= 20 THEN 'Normal'
                        WHEN i.Available_QTY >= 10 THEN 'Low'
                        ELSE 'Critical'
                    END AS Stock_Status
                FROM inventory i
                JOIN product p ON i.Product_ID=p.Product_ID
            """

            if filter_level == "Normal (≥20)":
                query += " WHERE i.Available_QTY >= 20"
            elif filter_level == "Low (10-19)":
                query += " WHERE i.Available_QTY >= 10 AND i.Available_QTY < 20"
            elif filter_level == "Critical (<10)":
                query += " WHERE i.Available_QTY < 10"

            query += " ORDER BY i.Available_QTY ASC"

            cursor.execute(query)
            rows=cursor.fetchall()

            for row in rows:
                status=row[4]
                if status == "Normal":
                    tree.insert("","end",values=row,tags=('normal',))
                elif status == "Low":
                    tree.insert("","end",values=row,tags=('low',))
                else:
                    tree.insert("","end",values=row,tags=('critical',))

            # Configure tag colors
            tree.tag_configure('normal',background='#27AE60',foreground='white')
            tree.tag_configure('low',background='#F39C12',foreground='white')
            tree.tag_configure('critical',background='#E74C3C',foreground='white')

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    load_stock_table()

    # Welcome message
    welcome_frame=tk.Frame(root,bg="#273746",padx=20,pady=8)
    welcome_frame.pack(side="bottom",fill="x",pady=8,padx=40)
    
    tk.Label(welcome_frame,
             text="💡 Welcome to Supply Chain Management System - Use the navigation bar to manage all aspects of your supply chain",
             font=("Arial",9,"bold"),bg="#273746",fg="#ECF0F1").pack()

    root.mainloop()
