import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox,ttk
from Cust_Dash import create_navbar

def open_shipments(cust_id):
    root=tk.Tk()
    root.title("Shipments & Invoices")
    root.geometry("900x700")
    root.resizable(False,False)
    root.configure(bg="#2C3E50")

    # Create navbar
    create_navbar(root,cust_id,"shipments")

    # Title
    title_label=tk.Label(root,text="My Shipments & Invoices",font=("Helvetica",24,"bold"),bg="#2C3E50",fg="#ECF0F1")
    title_label.pack(pady=20)

    # Shipments Table
    lbl_shipments=tk.Label(root,text="Shipments",font=("Arial",16,"bold"),bg="#2C3E50",fg="#ECF0F1")
    lbl_shipments.pack(pady=(10,5))

    ship_frame=tk.Frame(root,bg="#2C3E50")
    ship_frame.pack(pady=5,fill="both",expand=True,padx=20)

    ship_columns=("Shipment_ID","Order_ID","Shipment_Date","Status")
    ship_tree=ttk.Treeview(ship_frame,columns=ship_columns,show="headings",height=7)
    
    for col in ship_columns:
        ship_tree.heading(col,text=col)
        ship_tree.column(col,width=200,anchor="center")

    ship_scroll=ttk.Scrollbar(ship_frame,orient="vertical",command=ship_tree.yview)
    ship_tree.configure(yscrollcommand=ship_scroll.set)
    ship_scroll.pack(side="right",fill="y")
    ship_tree.pack(fill="both",expand=True)

    # Invoices Table
    lbl_invoices=tk.Label(root,text="Invoices",font=("Arial",16,"bold"),bg="#2C3E50",fg="#ECF0F1")
    lbl_invoices.pack(pady=(10,5))

    inv_frame=tk.Frame(root,bg="#2C3E50")
    inv_frame.pack(pady=5,fill="both",expand=True,padx=20)

    inv_columns=("Invoice_ID","Order_ID","Total_Amount","Invoice_Date")
    inv_tree=ttk.Treeview(inv_frame,columns=inv_columns,show="headings",height=7)
    
    for col in inv_columns:
        inv_tree.heading(col,text=col)
        inv_tree.column(col,width=200,anchor="center")

    inv_scroll=ttk.Scrollbar(inv_frame,orient="vertical",command=inv_tree.yview)
    inv_tree.configure(yscrollcommand=inv_scroll.set)
    inv_scroll.pack(side="right",fill="y")
    inv_tree.pack(fill="both",expand=True)

    def load_data():
        # Clear tables
        for item in ship_tree.get_children():
            ship_tree.delete(item)
        for item in inv_tree.get_children():
            inv_tree.delete(item)

        try:
            conn=mysql.connect(
                host="localhost",
                user="root",
                password="<Password> ",
                database="<Database to work on>"
            )
            cursor=conn.cursor()
            
            # Load shipments
            ship_query="""
            SELECT s.Shipment_ID,s.Order_ID,s.Shipment_Date,s.Status
            FROM shipment s
            JOIN orders o ON s.Order_ID=o.Order_ID
            WHERE o.Cust_ID=%s
            ORDER BY s.Shipment_Date DESC
            """
            cursor.execute(ship_query,(cust_id,))
            for row in cursor.fetchall():
                ship_tree.insert("","end",values=row)

            # Load invoices
            inv_query="""
            SELECT i.Invoice_ID,i.Order_ID,i.Total_Amount,i.Invoice_Date
            FROM invoice i
            JOIN orders o ON i.Order_ID=o.Order_ID
            WHERE o.Cust_ID=%s
            ORDER BY i.Invoice_Date DESC
            """
            cursor.execute(inv_query,(cust_id,))
            for row in cursor.fetchall():
                inv_tree.insert("","end",values=row)

            cursor.close()
            conn.close()
        except mysql.Error as e:
            messagebox.showerror("Database Error",f"Error: {e}")

    # Action Buttons
    action_frame=tk.Frame(root,bg="#2C3E50")
    action_frame.pack(pady=10)

    btn_refresh=tk.Button(action_frame,text="Refresh",font=("Arial",12),bg="#95A5A6",fg="white",
                            activebackground="#7F8C8D",command=load_data,width=12)
    btn_refresh.pack(side="left",padx=5)

    load_data()
    root.mainloop()

if __name__ == "__main__":
    open_shipments(1)