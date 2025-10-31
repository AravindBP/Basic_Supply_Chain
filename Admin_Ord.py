import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk


def open_admin_orders(admin_id):
    root=tk.Tk()
    root.title("Order Management")
    root.geometry("1400x900")
    root.resizable(False,False)
    root.configure(bg="#1C2833")

    # Create navbar with admin_id
    from Admin_Dash import create_admin_navbar
    create_admin_navbar(root,admin_id,"orders")

    # Title
    title_label=tk.Label(root,text="Order Management",font=("Helvetica",20,"bold"),
                          bg="#1C2833",fg="#9B59B6")
    title_label.pack(pady=12)

    # Search and Filter Frame
    filter_frame=tk.Frame(root,bg="#273746",padx=15,pady=10)
    filter_frame.pack(pady=8,fill="x",padx=20)

    lbl_search=tk.Label(filter_frame,text="Search Order:",font=("Arial",11),
                         bg="#273746",fg="#ECF0F1")
    lbl_search.pack(side="left",padx=8)

    entry_search=tk.Entry(filter_frame,font=("Arial",11),width=20)
    entry_search.pack(side="left",padx=5)

    def search_orders():
        load_orders(entry_search.get(),status_var.get())

    btn_search=tk.Button(filter_frame,text="🔍 Search",font=("Arial",10,"bold"),
                          bg="#3498DB",fg="white",command=search_orders,width=10)
    btn_search.pack(side="left",padx=5)

    # Status Filter
    tk.Label(filter_frame,text="Status:",font=("Arial",11),
            bg="#273746",fg="#ECF0F1").pack(side="left",padx=(20,5))

    status_var=tk.StringVar(value="All")
    combo_status=ttk.Combobox(filter_frame,textvariable=status_var,
                                values=["All","pending","dispatched","delivered","cancelled"],
                                font=("Arial",10),state="readonly",width=12)
    combo_status.pack(side="left",padx=5)

    def filter_by_status():
        load_orders(entry_search.get(),status_var.get())

    btn_filter=tk.Button(filter_frame,text="Apply Filter",font=("Arial",10,"bold"),
                          bg="#9B59B6",fg="white",command=filter_by_status,width=12)
    btn_filter.pack(side="left",padx=5)

    btn_refresh=tk.Button(filter_frame,text="🔄 Refresh",font=("Arial",10,"bold"),
                           bg="#95A5A6",fg="white",command=lambda: load_orders(),width=10)
    btn_refresh.pack(side="left",padx=5)

    # Separator - Delete Cancelled Order (moved to filter bar)
    separator=tk.Frame(filter_frame,bg="#7F8C8D",width=2,height=30)
    separator.pack(side="left",padx=15,pady=5)

    # Delete Order in Filter Bar
    lbl_delete=tk.Label(filter_frame,text="🗑️ Delete Cancelled:",font=("Arial",11,"bold"),
                         bg="#273746",fg="#E74C3C")
    lbl_delete.pack(side="left",padx=5)

    entry_delete_order_id=tk.Entry(filter_frame,font=("Arial",10),width=12)
    entry_delete_order_id.pack(side="left",padx=5)

    def delete_order():
        order_id=entry_delete_order_id.get().strip()
        if not order_id:
            messagebox.showerror("Error","Please enter Order ID")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password>",
                database="<Database to work on>"
            )
            cursor=conn.cursor()

            # Check if order exists and is cancelled (case-insensitive)
            cursor.execute("SELECT LOWER(Status),Product_ID,Qty FROM orders WHERE Order_ID=%s",(order_id,))
            result=cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error",f"Order ID '{order_id}' not found")
                cursor.close()
                conn.close()
                return

            status,product_id,qty=result
            status=status.lower()

            # Only allow deletion of cancelled orders
            if status != "cancelled":
                messagebox.showerror("Error",
                                   f"Cannot delete order!\n\n"
                                   f"Current Status: {status}\n\n"
                                   f"Only 'cancelled' orders can be deleted.\n"
                                   f"Please cancel the order first.")
                cursor.close()
                conn.close()
                return

            confirm=messagebox.askyesno("Confirm Delete",
                                          f"Delete cancelled order '{order_id}'?\n\n"
                                          f"This will also delete:\n"
                                          f"Associated shipment record\n"
                                          f"Associated invoice record\n\n"
                                          f"This action cannot be undone!")
            if not confirm:
                cursor.close()
                conn.close()
                return

            # Delete in order: invoice → shipment → order
            # 1. Delete invoice
            cursor.execute("DELETE FROM invoice WHERE Order_ID=%s",(order_id,))
            invoice_deleted=cursor.rowcount
            
            # 2. Delete shipment
            cursor.execute("DELETE FROM shipment WHERE Order_ID=%s",(order_id,))
            shipment_deleted=cursor.rowcount
            
            # 3. Delete order
            cursor.execute("DELETE FROM orders WHERE Order_ID=%s",(order_id,))
            
            conn.commit()
            
            messagebox.showinfo("✅ Order Deleted Successfully!",
                               f"Order Deletion Complete!\n\n"
                               f"Order ID: {order_id}\n"
                               f"Status: cancelled\n\n"
                               f"Deleted Records:\n"
                               f"• Order:\n"
                               f"• Shipment: {'' if shipment_deleted > 0 else '(not found)'}\n"
                               f"• Invoice: {'' if invoice_deleted > 0 else '(not found)'}")
            
            entry_delete_order_id.delete(0,tk.END)
            load_orders()

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_delete=tk.Button(filter_frame,text="Delete Order",font=("Arial",10,"bold"),
                          bg="#E74C3C",fg="white",command=delete_order,width=12)
    btn_delete.pack(side="left",padx=5)

    # Orders Table
    table_frame=tk.Frame(root,bg="#1C2833")
    table_frame.pack(pady=8,fill="both",expand=False,padx=20)

    columns=("Order_ID","Order_Date","Customer_ID","Product_ID","Qty","Status","Total_Cost")
    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=10)

    tree.heading("Order_ID",text="Order ID")
    tree.heading("Order_Date",text="Order Date")
    tree.heading("Customer_ID",text="Customer ID")
    tree.heading("Product_ID",text="Product ID")
    tree.heading("Qty",text="Quantity")
    tree.heading("Status",text="Status")
    tree.heading("Total_Cost",text="Total Cost")

    tree.column("Order_ID",width=100,anchor="center")
    tree.column("Order_Date",width=120,anchor="center")
    tree.column("Customer_ID",width=120,anchor="center")
    tree.column("Product_ID",width=120,anchor="center")
    tree.column("Qty",width=100,anchor="center")
    tree.column("Status",width=120,anchor="center")
    tree.column("Total_Cost",width=130,anchor="center")

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True)

    def load_orders(search_term="",status_filter="All"):
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password>",
                database="<Database to work on>"
            )
            cursor=conn.cursor()

            query="""
                SELECT 
                    Order_ID,
                    Order_Date,
                    Cust_ID,
                    Product_ID,
                    Qty,
                    Status,
                    GetOrderTotalCost(Order_ID) as Total_Cost
                FROM orders
                WHERE 1=1
            """

            params=[]

            if search_term:
                query += " AND (Order_ID LIKE %s OR Cust_ID LIKE %s OR Product_ID LIKE %s)"
                params.extend([f"%{search_term}%",f"%{search_term}%",f"%{search_term}%"])

            if status_filter != "All":
                query += " AND LOWER(Status)=%s"
                params.append(status_filter.lower())

            query += " ORDER BY Order_Date DESC"

            cursor.execute(query,params) if params else cursor.execute(query)

            rows=cursor.fetchall()
            for row in rows:
                order_list=list(row)
                status=order_list[5].lower() if order_list[5] else ""
                
                # Format total cost
                if order_list[6] is not None:
                    order_list[6]=f"${order_list[6]:.2f}"
                else:
                    order_list[6]="N/A"
                
                # Color code based on status
                if status == "pending":
                    tree.insert("","end",values=order_list,tags=('pending',))
                elif status == "dispatched":
                    tree.insert("","end",values=order_list,tags=('dispatched',))
                elif status == "delivered":
                    tree.insert("","end",values=order_list,tags=('delivered',))
                elif status == "cancelled":
                    tree.insert("","end",values=order_list,tags=('cancelled',))
                else:
                    tree.insert("","end",values=order_list)

            # Configure tag colors
            tree.tag_configure('pending',background='#F39C12',foreground='white')
            tree.tag_configure('dispatched',background='#3498DB',foreground='white')
            tree.tag_configure('delivered',background='#27AE60',foreground='white')
            tree.tag_configure('cancelled',background='#E74C3C',foreground='white')

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Operations Container
    operations_frame=tk.Frame(root,bg="#1C2833")
    operations_frame.pack(pady=8,fill="both",expand=True,padx=20)

    # Left Column: Update Order Status
    left_column=tk.Frame(operations_frame,bg="#1C2833")
    left_column.pack(side="left",fill="both",expand=True,padx=(0,10))

    # Update Status Frame
    update_frame=tk.Frame(left_column,bg="#273746",padx=18,pady=15)
    update_frame.pack(fill="both",expand=True)

    tk.Label(update_frame,text="📝 Update Order Status",
             font=("Arial",12,"bold"),bg="#273746",fg="#3498DB").pack(pady=(0,15))

    input_frame=tk.Frame(update_frame,bg="#273746")
    input_frame.pack(pady=10)

    tk.Label(input_frame,text="Order ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=0,column=0,padx=8,pady=8,sticky="e")
    entry_order_id=tk.Entry(input_frame,font=("Arial",10),width=18)
    entry_order_id.grid(row=0,column=1,padx=8,pady=8)

    tk.Label(input_frame,text="New Status:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=1,column=0,padx=8,pady=8,sticky="e")
    
    status_update_var=tk.StringVar(value="pending")
    combo_new_status=ttk.Combobox(input_frame,textvariable=status_update_var,
                                    values=["pending","dispatched","delivered","cancelled"],
                                    font=("Arial",10),state="readonly",width=16)
    combo_new_status.grid(row=1,column=1,padx=8,pady=8)

    def update_order_status():
        order_id=entry_order_id.get().strip()
        new_status=status_update_var.get().lower()

        if not order_id:
            messagebox.showerror("Error","Please enter Order ID")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password>",
                database="<Database to work on>"
            )
            cursor=conn.cursor()

            # Check if order exists (case-insensitive)
            cursor.execute("SELECT LOWER(Status),Product_ID,Qty FROM orders WHERE Order_ID=%s",(order_id,))
            result=cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error",f"Order ID '{order_id}' not found")
                cursor.close()
                conn.close()
                return

            old_status,product_id,qty=result
            old_status=old_status.lower()

            if old_status == new_status:
                messagebox.showinfo("Info",f"Order is already in '{new_status}' status")
                cursor.close()
                conn.close()
                return

            # Validate status transitions
            if old_status == "cancelled":
                messagebox.showerror("Error","Cannot update status of cancelled orders")
                cursor.close()
                conn.close()
                return

            if old_status == "delivered" and new_status != "cancelled":
                messagebox.showerror("Error","Cannot change status of delivered orders (except cancellation)")
                cursor.close()
                conn.close()
                return

            # Update the status
            cursor.execute("UPDATE orders SET Status=%s WHERE Order_ID=%s",(new_status,order_id))

            # Update shipment status as well
            if new_status == "cancelled":
                cursor.execute("UPDATE shipment SET Status='Cancelled' WHERE Order_ID=%s",(order_id,))
            elif new_status == "dispatched":
                cursor.execute("UPDATE shipment SET Status='Dispatched' WHERE Order_ID=%s",(order_id,))
            elif new_status == "delivered":
                cursor.execute("UPDATE shipment SET Status='Delivered' WHERE Order_ID=%s",(order_id,))

            # Handle inventory changes based on status
            if new_status == "cancelled" and old_status != "cancelled":
                # Restore inventory
                cursor.execute("""
                    UPDATE inventory 
                    SET 
                        Available_QTY=Available_QTY + %s,
                        Reserved_QTY=Reserved_QTY - %s
                    WHERE Product_ID=%s
                """,(qty,qty,product_id))
                
            elif new_status == "dispatched" and old_status == "pending":
                # Move from reserved to in-transit
                cursor.execute("""
                    UPDATE inventory 
                    SET 
                        Reserved_QTY=Reserved_QTY - %s,
                        In_Transit_Qty=In_Transit_Qty + %s
                    WHERE Product_ID=%s
                """,(qty,qty,product_id))
                
            elif new_status == "delivered" and old_status == "dispatched":
                # Remove from in-transit
                cursor.execute("""
                    UPDATE inventory 
                    SET In_Transit_Qty=In_Transit_Qty - %s
                    WHERE Product_ID=%s
                """,(qty,product_id))

            conn.commit()
            messagebox.showinfo("Success",
                               f"Order Status Updated!\n\n"
                               f"Order ID: {order_id}\n"
                               f"Old Status: {old_status}\n"
                               f"New Status: {new_status}\n"
                               f"Shipment status updated accordingly")
            
            entry_order_id.delete(0,tk.END)
            load_orders()

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_update=tk.Button(update_frame,text="📝 Update Status",font=("Arial",11,"bold"),
                          bg="#3498DB",fg="white",command=update_order_status,width=18,height=2)
    btn_update.pack(pady=15)

    # Status Flow Info
    info_label=tk.Label(update_frame,
                         text="📋 Status Flow:\npending → dispatched → delivered\n\n"
                              "⚠️ cancelled orders cannot be updated\n"
                              "✅ delivered orders can only be cancelled",
                         font=("Arial",9,"italic"),bg="#273746",fg="#ECF0F1",
                         justify="left")
    info_label.pack(pady=(10,0))

    # Right Column: View Order Details
    right_column=tk.Frame(operations_frame,bg="#1C2833")
    right_column.pack(side="right",fill="both",expand=True,padx=(10,0))

    # View Details Frame
    view_frame=tk.Frame(right_column,bg="#273746",padx=18,pady=15)
    view_frame.pack(fill="both",expand=True)

    tk.Label(view_frame,text="🔍 View Order Details",
             font=("Arial",12,"bold"),bg="#273746",fg="#27AE60").pack(pady=(0,15))

    input_frame_view=tk.Frame(view_frame,bg="#273746")
    input_frame_view.pack(pady=10)

    tk.Label(input_frame_view,text="Order ID:",font=("Arial",10),
             bg="#273746",fg="#ECF0F1").grid(row=0,column=0,padx=8,pady=8,sticky="e")
    entry_view_order_id=tk.Entry(input_frame_view,font=("Arial",10),width=18)
    entry_view_order_id.grid(row=0,column=1,padx=8,pady=8)

    def view_order_details():
        order_id=entry_view_order_id.get().strip()
        
        if not order_id:
            messagebox.showerror("Error","Please enter Order ID")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password>",
                database="<Database to work on>"
            )
            cursor=conn.cursor()

            # Call ShowOrders stored procedure
            cursor.callproc('ShowOrders',[order_id])
            
            # Fetch results from the procedure
            for result in cursor.stored_results():
                order_details=result.fetchone()
                
                if order_details:
                    details_text=f"""
╔══════════════════════════════════╗
         ORDER DETAILS
╚══════════════════════════════════╝

Order ID:        {order_details[0]}
Order Date:      {order_details[1]}
Product ID:      {order_details[2]}
Status:          {order_details[3]}
Customer ID:     {order_details[4]}
Quantity:        {order_details[5]}
Total Cost:      ${order_details[6]:.2f}

────────────────────────────────────
                    """
                    messagebox.showinfo("Order Details",details_text)
                else:
                    messagebox.showerror("Error","Order not found")

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_view=tk.Button(view_frame,text="🔍 View Details",font=("Arial",11,"bold"),
                        bg="#27AE60",fg="white",command=view_order_details,width=18,height=2)
    btn_view.pack(pady=15)

    load_orders()
    root.mainloop()
