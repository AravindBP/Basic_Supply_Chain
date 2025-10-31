import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk
from Cust_Dash import create_navbar


def open_orders(cust_id):
    root=tk.Tk()
    root.title("My Orders")
    root.geometry("1100x700")
    root.resizable(False,False)
    root.configure(bg="#2C3E50")

    # Create navbar
    create_navbar(root,cust_id,"orders")

    # Title
    title_label=tk.Label(root,text="My Orders",font=("Helvetica",24,"bold"),
                          bg="#2C3E50",fg="#ECF0F1")
    title_label.pack(pady=20)

    # Filter Frame with Cancel Order Option
    filter_frame=tk.Frame(root,bg="#34495E",padx=10,pady=10)
    filter_frame.pack(pady=10,fill="x",padx=20)

    # Left side: Filter by Status
    lbl_status=tk.Label(filter_frame,text="Filter by Status:",font=("Arial",11),
                         bg="#34495E",fg="#ECF0F1")
    lbl_status.pack(side="left",padx=5)

    status_var=tk.StringVar(value="All")
    combo_status=ttk.Combobox(filter_frame,textvariable=status_var,
                                values=["All","pending","dispatched","delivered","cancelled"],
                                font=("Arial",10),state="readonly",width=12)
    combo_status.pack(side="left",padx=5)

    def filter_orders():
        load_orders(status_var.get())

    btn_filter=tk.Button(filter_frame,text="Apply Filter",font=("Arial",10),
                          bg="#3498DB",fg="white",command=filter_orders,width=10)
    btn_filter.pack(side="left",padx=5)

    btn_refresh=tk.Button(filter_frame,text="🔄 Refresh",font=("Arial",10),
                           bg="#95A5A6",fg="white",command=lambda: load_orders(),width=10)
    btn_refresh.pack(side="left",padx=5)

    # Separator
    separator=tk.Frame(filter_frame,bg="#7F8C8D",width=2,height=30)
    separator.pack(side="left",padx=10,pady=5)

    # Right side: Cancel Order
    lbl_cancel=tk.Label(filter_frame,text="❌ Cancel Order:",font=("Arial",11,"bold"),
                         bg="#34495E",fg="#E74C3C")
    lbl_cancel.pack(side="left",padx=5)

    entry_cancel_order=tk.Entry(filter_frame,font=("Arial",10),width=12)
    entry_cancel_order.pack(side="left",padx=5)

    def cancel_order():
        order_id=entry_cancel_order.get().strip()
        
        if not order_id:
            messagebox.showerror("Error","Please enter Order ID")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            # Check if order exists and belongs to customer (case-insensitive status check)
            cursor.execute("""
                SELECT LOWER(Status),Product_ID,Qty 
                FROM orders 
                WHERE Order_ID=%s AND Cust_ID=%s
            """,(order_id,cust_id))
            
            result=cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error","Order not found or doesn't belong to you")
                cursor.close()
                conn.close()
                return

            status,product_id,qty=result
            status=status.lower()  # Normalize to lowercase

            # Only allow cancellation for pending orders
            if status != "pending":
                messagebox.showerror("Error",
                                   f"Cannot cancel order!\n\n"
                                   f"Current Status: {status}\n\n"
                                   f"Only 'pending' orders can be cancelled.\n"
                                   f"Orders that are 'dispatched' or 'delivered' cannot be cancelled.")
                cursor.close()
                conn.close()
                return

            # Confirm cancellation
            confirm=messagebox.askyesno("Confirm Cancellation",
                                         f"Cancel Order {order_id}?\n\n"
                                         f"Product ID: {product_id}\n"
                                         f"Quantity: {qty}\n\n"
                                         f"This action cannot be undone!")
            if not confirm:
                cursor.close()
                conn.close()
                return

            # Cancel the order (case-insensitive)
            cursor.execute("""
                UPDATE orders 
                SET Status='cancelled' 
                WHERE Order_ID=%s AND LOWER(Status)='pending'
            """,(order_id,))

            # Cancel the associated shipment (case-insensitive)
            cursor.execute("""
                UPDATE shipment 
                SET Status='Cancelled' 
                WHERE Order_ID=%s AND LOWER(Status)='pending'
            """,(order_id,))

            # Restore inventory (move from Reserved back to Available)
            cursor.execute("""
                UPDATE inventory 
                SET 
                    Available_QTY=Available_QTY + %s,
                    Reserved_QTY=Reserved_QTY - %s
                WHERE Product_ID=%s
            """,(qty,qty,product_id))

            conn.commit()
            
            messagebox.showinfo("✅ Order Cancelled",
                               f"Order Cancellation Successful!\n\n"
                               f"Order ID: {order_id}\n"
                               f"Product ID: {product_id}\n"
                               f"Quantity Restored: {qty} units\n\n"
                               f"📦 Inventory updated (Available +{qty},Reserved -{qty})\n"
                               f"🚚 Shipment marked as cancelled")
            
            entry_cancel_order.delete(0,tk.END)
            load_orders()

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    btn_cancel=tk.Button(filter_frame,text="Cancel Order",font=("Arial",10,"bold"),
                          bg="#E74C3C",fg="white",command=cancel_order,width=12)
    btn_cancel.pack(side="left",padx=5)

    # Orders Table
    table_frame=tk.Frame(root,bg="#2C3E50")
    table_frame.pack(pady=10,fill="both",expand=True,padx=20)

    columns=("Order_ID","Product_ID","Qty","Order_Date","Status","Total_Cost")
    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=15)

    tree.heading("Order_ID",text="Order ID")
    tree.heading("Product_ID",text="Product ID")
    tree.heading("Qty",text="Quantity")
    tree.heading("Order_Date",text="Order Date")
    tree.heading("Status",text="Status")
    tree.heading("Total_Cost",text="Total Cost")

    tree.column("Order_ID",width=120,anchor="center")
    tree.column("Product_ID",width=120,anchor="center")
    tree.column("Qty",width=100,anchor="center")
    tree.column("Order_Date",width=150,anchor="center")
    tree.column("Status",width=130,anchor="center")
    tree.column("Total_Cost",width=150,anchor="center")

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True)

    def load_orders(status_filter="All"):
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

            # Get all orders for this customer using the GetOrderTotalCost function
            query="""
                SELECT Order_ID,Product_ID,Qty,Order_Date,Status,
                       GetOrderTotalCost(Order_ID) as Total_Cost
                FROM orders
                WHERE Cust_ID=%s
            """

            if status_filter != "All":
                query += " AND LOWER(Status)=%s"
                query += " ORDER BY Order_Date DESC"
                cursor.execute(query,(cust_id,status_filter.lower()))
            else:
                query += " ORDER BY Order_Date DESC"
                cursor.execute(query,(cust_id,))

            orders=cursor.fetchall()

            for order in orders:
                # Format the total cost and apply color coding
                order_list=list(order)
                status=order_list[4].lower() if order_list[4] else ""
                
                if order_list[5] is not None:
                    order_list[5]=f"${order_list[5]:.2f}"
                else:
                    order_list[5]="N/A"
                
                # Color code based on status (case-insensitive)
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

    # View Order Details Frame (Using ShowOrders Stored Procedure)
    detail_frame=tk.Frame(root,bg="#34495E",padx=20,pady=15)
    detail_frame.pack(pady=10,fill="x",padx=20)

    tk.Label(detail_frame,text="🔍 View Order Details",
             font=("Arial",12,"bold"),bg="#34495E",fg="#3498DB").pack(pady=5)

    input_frame=tk.Frame(detail_frame,bg="#34495E")
    input_frame.pack(pady=5)

    tk.Label(input_frame,text="Enter Order ID:",font=("Arial",11),
             bg="#34495E",fg="#ECF0F1").pack(side="left",padx=5)
    entry_order_id=tk.Entry(input_frame,font=("Arial",11),width=15)
    entry_order_id.pack(side="left",padx=5)

    def view_order_details():
        order_id=entry_order_id.get().strip()
        
        if not order_id:
            messagebox.showerror("Error","Please enter Order ID")
            return

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on> "
            )
            cursor=conn.cursor()

            # Call ShowOrders stored procedure
            cursor.callproc('ShowOrders',[order_id])
            
            # Fetch results from the procedure
            for result in cursor.stored_results():
                order_details=result.fetchone()
                
                if order_details:
                    # Verify this order belongs to the logged-in customer
                    if order_details[4] != cust_id:
                        messagebox.showerror("Error","There is no such order associated to your account")
                        cursor.close()
                        conn.close()
                        return

                    details_text=f"""
╔══════════════════════════════════╗
         ORDER DETAILS
╚══════════════════════════════════╝

Order ID:        {order_details[0]}
Order Date:      {order_details[1]}
Product ID:      {order_details[2]}
Status:          {order_details[3]}
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

    btn_view=tk.Button(input_frame,text="View Details",font=("Arial",11,"bold"),
                        bg="#3498DB",fg="white",command=view_order_details,width=15)
    btn_view.pack(side="left",padx=10)

    load_orders()
    root.mainloop()
