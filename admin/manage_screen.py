from .admin_base import AdminBase
import mysql.connector as sql
import numpy as np
from rich.console import Console
from rich.table import Table
class ManageScreen(AdminBase):
    def __init__(self, theatre_id):
        super().__init__()
        self.theatre_id = theatre_id
        self.screen_menu()

    def screen_menu(self):
        while True:
            print(f"\n🎭 Managing Screens for Theatre ID: {self.theatre_id}")
            # print("\t\t1. Add Screen")
            # print("\t\t1. Remove Screen")
            print("\t\t1. Update Screen")
            print("\t\t2. View All Screens")
            print("\t\t3. View Seat Availability")
            print("\t\t4. Back to Theatre Management")
            
            choice = input("👉 Enter your choice: ")

            if choice == "1":
            #     self.add_screen()
            # elif choice == "2":
            #     self.remove_screen()
            # elif choice == "3":
                self.update_screen()
            elif choice == "2":
                self.view_all_screens()
            elif choice == "3":
                self.view_availability()
            elif choice == "4":
                print("\n🔙 Returning to Theatre Management...")
                break
            else:
                print("⚠️ Invalid choice. Please try again.")

    # def add_screen(self):
    #     try:
    #         screen_id = input("Enter Screen ID: ")
    #         no_row_gold = int(input("Enter Number of Rows for Gold Class: "))
    #         no_col_gold = int(input("Enter Number of Columns for Gold Class: "))
    #         availability_gold = input("Enter Availability for Gold Class (1 for available, 0 for booked, separated by space): ")
    #         no_row_silver = int(input("Enter Number of Rows for Silver Class: "))
    #         no_col_silver = int(input("Enter Number of Columns for Silver Class: "))
    #         availability_silver = input("Enter Availability for Silver Class (1 for available, 0 for booked, separated by space): ")

    #         query = """
    #             INSERT INTO Screen (Screen_ID, Theatre_ID, No_Row_Gold, No_Col_Gold, Availability_Gold, 
    #                                 No_Row_Silver, No_Col_Silver, Availability_Silver)
    #             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    #         """
    #         values = (screen_id, self.theatre_id, no_row_gold, no_col_gold, availability_gold, no_row_silver, no_col_silver, availability_silver)
    #         self.cursor.execute(query, values)
    #         self.connection.commit()
    #         print("\n✅ Screen added successfully.")
    #     except sql.Error as e:
    #         print("❌ Error adding screen:", e)


    def remove_screen(self):
        try:
            screen_id = input("Enter Screen ID to remove: ")
            query = "DELETE FROM screen WHERE Screen_ID = %s AND Theatre_ID = %s ;"
            self.cursor.execute(query, (screen_id, self.theatre_id))
            self.connection.commit()
            print("\n✅ Screen removed successfully.")
        except sql.Error as e:
            print("❌ Error removing screen:", e)

    def update_screen(self):
        try:
            screen_id = input("Enter Screen ID to update: ").upper()
            no_row_gold = int(input("Enter new Number of Rows for Gold Class: "))
            no_col_gold = int(input("Enter new Number of Columns for Gold Class: "))
            no_row_silver = int(input("Enter new Number of Rows for Silver Class: "))
            no_col_silver = int(input("Enter new Number of Columns for Silver Class: "))
            
            # Creating the availability strings
            Availability_Gold = '1' * (no_col_gold * no_row_gold)
            Availability_Silver = '1' * (no_col_silver * no_row_silver)

            query = """
                UPDATE screen
                SET No_Row_Gold = %s, No_Col_Gold = %s, 
                    No_Row_Silver = %s, No_Col_Silver = %s, Availability_Gold = %s, Availability_Silver = %s
                WHERE Screen_ID = %s;
            """
            values = (no_row_gold, no_col_gold, no_row_silver, no_col_silver, Availability_Gold, Availability_Silver, screen_id)
            
            self.cursor.execute(query, values)
            self.connection.commit()

            # Check if any row was affected
            if self.cursor.rowcount > 0:
                print("\n✅ Screen updated successfully.")
            else:
                print('⚠️ No changes made. Screen ID not found or already updated.')

        except sql.Error as e:
            print("❌ Error updating screen:", e)


    def view_all_screens(self):
        try:
            query = "SELECT * FROM screen WHERE Theatre_ID = %s ;"
            self.cursor.execute(query, (self.theatre_id,))
            screens = self.cursor.fetchall()

            console = Console()

            
            table = Table(title=f"📜 Screens for Theatre ID: {self.theatre_id}", show_lines=True)

            # Define table columns
            table.add_column("Screen ID", justify="center", style="blue")
            table.add_column("Gold Rows", justify="center", style="green")
            table.add_column("Gold Columns", justify="center", style="yellow")
            table.add_column("Silver Rows", justify="center", style="magenta")
            table.add_column("Silver Columns", justify="center", style="cyan")

            
            for screen in screens:
                table.add_row(
                    str(screen[0]),  # Screen ID
                    str(screen[2]),  # Gold Rows
                    str(screen[3]),  # Gold Columns
                    str(screen[5]),  # Silver Rows
                    str(screen[6])   # Silver Columns
                )

            
            console.print(table)

        except sql.Error as e:
            print("❌ Error fetching screens:", e)

    def view_availability(self):
        try:
            screen_id = input("Enter Screen ID to view availability: ")
            
            query = "SELECT No_Row_Gold, No_Col_Gold, Availability_Gold, No_Row_Silver, No_Col_Silver, Availability_Silver " \
                    "FROM screen WHERE Screen_ID = %s AND Theatre_ID = %s ;"
            self.cursor.execute(query, (screen_id, self.theatre_id))
            result = self.cursor.fetchone()

            if result:
                row_gold = int(result[0])
                col_gold = int(result[1])
                availability_gold = list(result[2])
                row_silver = int(result[3])
                col_silver = int(result[4])
                availability_silver = list(result[5])

                gold_matrix = np.array(availability_gold).reshape(row_gold, col_gold)
                silver_matrix = np.array(availability_silver).reshape(row_silver, col_silver)

                print("\n🎟️ Gold Class Availability for Screen ID:", screen_id)
                self.print_seat_matrix(gold_matrix, row_gold, col_gold)

                print("\n🎟️ Silver Class Availability for Screen ID:", screen_id)
                self.print_seat_matrix(silver_matrix, row_silver, col_silver)

            else:
                print("❌ Screen not found.")
        except sql.Error as e:
            print("❌ Error fetching availability:", e)

    def print_seat_matrix(self, matrix, rows, cols):
        for i in range(rows):
            for j in range(cols):
                seat = matrix[i][j]
                if seat == '1':  
                    print(f"\u001B[32m{chr(i+65)}{j}\u001B[0m", end=" ")  
                else:  
                    print(f"\u001B[31mXX\u001B[0m", end=" ")  
            print()