from .admin_base import AdminBase
import mysql.connector as sql
from rich.console import Console
from rich.table import Table
class ManageBooking(AdminBase):
    
    def __init__(self, theatre_id):
        super().__init__()
        self.theatre_id = theatre_id
        self.booking_menu()

    def booking_menu(self):
        while True:
            print("\n\t\t---- Booking Panel - Theatre: ", self.theatre_id, " ----")
            print("\t\t\t1. View All Bookings")
            print("\t\t\t2. Update Booking")
            print("\t\t\t3. Exit")
            
            choice = input("👉 Enter your choice: ")

            if choice == "1":
                self.view_bookings()

            elif choice == "2":
                self.update_booking()  

            elif choice == "3":
                print("\n👋 Exiting Booking Panel...")
                break
            
            else:
                print("⚠️ Invalid choice. Please try again.")

    def view_bookings(self):
        try:
            query = """
                SELECT B.Booking_ID, U.First_Name, U.Last_Name, S.Show_Date, S.Show_Time, 
                       B.No_of_Tickets, B.Total_Cost 
                FROM booking B
                JOIN web_user U ON B.User_ID = U.Web_User_ID
                JOIN show_table S ON B.Show_ID = S.Show_ID
                JOIN screen SC ON S.Screen_ID = SC.Screen_ID
                JOIN theatre T ON SC.Theatre_ID = T.Theatre_ID
                WHERE T.Theatre_ID = %s
                ORDER BY S.Show_Date, S.Show_Time ;
            """
            self.cursor.execute(query, (self.theatre_id,))
            bookings = self.cursor.fetchall()

            if not bookings:
                print("\n🚫 No bookings found for this theatre.")
                return

            
            console = Console()

            
            table = Table(title="📜 Bookings List", show_lines=True)

            
            table.add_column("No.", justify="center", style="cyan", no_wrap=True)
            table.add_column("Booking ID", justify="center", style="blue")
            table.add_column("User", justify="left", style="magenta")
            table.add_column("Show Date", justify="center", style="green")
            table.add_column("Show Time", justify="center", style="yellow")
            table.add_column("Tickets", justify="center", style="red")
            table.add_column("Total Cost", justify="center", style="bold cyan")

            
            for i, booking in enumerate(bookings):
                user_name = f"{booking[1]} {booking[2]}"  # Combine First Name and Last Name
                table.add_row(
                    str(i),         # Serial No.
                    str(booking[0]), # Booking ID
                    user_name,       # User (First + Last Name)
                    str(booking[3]), # Show Date
                    str(booking[4]), # Show Time
                    str(booking[5]), # Number of Tickets
                    str(booking[6])  # Total Cost
                )

            # Print the table
            console.print(table)

        except sql.Error as e:
            print("❌ Error fetching bookings:", e)

    def update_booking(self):
        try:
            print("\n📝 Update Booking Details:")
            print("Leave blank if no change.")

            new_no_of_tickets = input("Enter New Number of Tickets (Leave blank to keep current): ")
            new_total_cost = input("Enter New Total Cost (Leave blank to keep current): ")
            new_card_number = input("Enter New Card Number (Leave blank to keep current): ")
            new_name_on_card = input("Enter New Name on Card (Leave blank to keep current): ")

            update_query = "UPDATE booking SET "
            update_values = []
            
            if new_no_of_tickets:
                update_query += "No_of_Tickets = %s, "
                update_values.append(int(new_no_of_tickets))

            if new_total_cost:
                update_query += "Total_Cost = %s, "
                update_values.append(int(new_total_cost))
            
            if new_card_number:
                update_query += "Card_Number = %s, "
                update_values.append(new_card_number)
            
            if new_name_on_card:
                update_query += "Name_on_card = %s, "
                update_values.append(new_name_on_card)
            
            update_query = update_query.rstrip(", ")

            update_query += " WHERE Booking_ID = %s ;"

            booking_id = input('👉 Enter booking ID:')
            update_values.append(booking_id)

            self.cursor.execute(update_query, tuple(update_values))
            self.connection.commit()

            print("\n✅ Booking updated successfully.")

        except sql.Error as e:
            print("❌\u001B[31m Error updating booking \u001B[0m")