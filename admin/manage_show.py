from .admin_base import AdminBase
import mysql.connector as sql
from rich.console import Console
from rich.table import Table
class ManageShow(AdminBase):
    def __init__(self, theatre_id):
        super().__init__()
        self.theatre_id = theatre_id
        self.screen_ids = self.get_screen_ids()
        self.movie_ids = self.get_movie_ids()
        self.show_menu()

    def get_screen_ids(self):
        """Fetch available screen IDs for the selected theatre."""
        try:
            query = "SELECT Screen_ID FROM screen WHERE Theatre_ID = %s;"
            self.cursor.execute(query, (self.theatre_id,))
            screen_ids = [screen[0] for screen in self.cursor.fetchall()]
            if not screen_ids:
                print("🚫 No screens found for this theatre.")
            return screen_ids
        except sql.Error as e:
            print("❌ Error fetching screen IDs:", e)
            return []

    def get_movie_ids(self):
        try:
            query = "SELECT DISTINCT Movie_ID FROM show_table;"
            self.cursor.execute(query)
            screen_ids = [screen[0] for screen in self.cursor.fetchall()]
            if not screen_ids:
                print("🚫 No screens found for this theatre.")
            return screen_ids
        except sql.Error as e:
            print("❌ Error fetching screen IDs:", e)
            return []

    def show_menu(self):
        while True:
            print("\n\t\t---- Show Management - Theatre ID:", self.theatre_id, "----")
            print("\t\t\t1.View Shows")
            print("\t\t\t2.Add Show")
            print("\t\t\t3.Update Show")
            print("\t\t\t4.Remove Show")
            print("\t\t\t5.Go Back to Theatre Menu")

            choice = input("👉 Enter your choice: ")

            if choice == "1":
                self.view_shows()
            elif choice == "2":
                self.add_show()
            elif choice == "3":
                self.update_show()
            elif choice == "4":
                self.remove_show()
            elif choice == "5":
                print("\n🔙 Returning to Theatre Menu...")
                break
            else:
                print("⚠️ Invalid choice. Please try again.")

    def view_shows(self):
        try:
            if not self.screen_ids:
                print("🚫 No screens available for this theatre.")
                return

            placeholders = ', '.join(['%s'] * len(self.screen_ids))
            query = f"""
                SELECT Show_ID, Show_Time, Show_Date, Seats_Remaining_Gold, Seats_Remaining_Silver,
                    Class_Cost_Gold, Class_Cost_Silver,Screen_ID, Movie_ID
                FROM show_table
                WHERE Screen_ID IN ({placeholders})
                ORDER BY Show_Date, Show_Time ;
            """

            self.cursor.execute(query, tuple(self.screen_ids))
            shows = self.cursor.fetchall()

            if not shows:
                print("🚫 No shows found for the selected screens in this theatre.")
                return

            
            console = Console()

            
            table = Table(title=f"🎬 Shows List for Theatre ID: {self.theatre_id}", show_lines=True)

            
            table.add_column("Show ID", justify="center", style="cyan", no_wrap=True)
            table.add_column("Time", justify="center", style="magenta")
            table.add_column("Date", justify="center", style="magenta")
            table.add_column("Gold Seats", justify="right", style="green")
            table.add_column("Silver Seats", justify="right", style="green")
            table.add_column("Gold Cost", justify="right", style="yellow")
            table.add_column("Silver Cost", justify="right", style="yellow")
            table.add_column("Screen ID", justify="center", style="blue")
            table.add_column("Movie ID", justify="center", style="red")

            # Add rows to the table
            for show in shows:
                table.add_row(
                    str(show[0]),  # Show ID
                    str(show[1]),  # Time
                    str(show[2]),  # Date
                    str(show[3]),  # Gold Seats
                    str(show[4]),  # Silver Seats
                    str(show[5]),  # Gold Cost
                    str(show[6]),  # Silver Cost
                    str(show[7]),  # Screen ID
                    str(show[8])   # Movie ID
                )

            # Print the table
            console.print(table)

        except sql.Error as e:
            print("❌ Error fetching shows:", e)

    def add_show(self):
        try:
            print("\n📝 Add New Show")

            show_time = input("Enter Show Time (HH:MM:SS): ")
            show_date = input("Enter Show Date (YYYY-MM-DD): ")
            seats_gold = int(input("Enter Gold Seats Remaining: "))
            seats_silver = int(input("Enter Silver Seats Remaining: "))
            cost_gold = int(input("Enter Gold Class Cost: "))
            cost_silver = int(input("Enter Silver Class Cost: "))

            if not self.screen_ids:
                print("🚫 No screens available for this theatre.")
                return

            print("\nAvailable Screen IDs:", self.screen_ids)
            screen_id = input("Enter Screen ID from the above list: ").upper()

            if screen_id not in self.screen_ids:
                print("⚠️ Invalid Screen ID.")
                return

            if not self.movie_ids:
                print("🚫 No Movies available for this theatre.")
                return

            print("\nAvailable Movie IDs:", self.movie_ids)
            movie_id = input("Enter Movie ID: ")

            if movie_id not in self.movie_ids:
                print("⚠️ Invalid Movie ID.")
                return

            query = """
                SELECT Show_ID FROM show_table WHERE Screen_ID = %s ORDER BY Show_ID DESC LIMIT 1;
            """
            self.cursor.execute(query, (screen_id,))
            result = self.cursor.fetchone()

            if result:
                last_show_id = result[0]
                number_part = int(last_show_id[6:])
                new_number = str(number_part + 1).zfill(4)
            else:
                new_number = "0001"

            new_show_id = f"SH{screen_id}{new_number}"

            query = """
                INSERT INTO show_table (Show_ID, Show_Time, Show_Date, Seats_Remaining_Gold, Seats_Remaining_Silver,
                                        Class_Cost_Gold, Class_Cost_Silver, Screen_ID, Movie_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(query, (new_show_id, show_time, show_date, seats_gold, seats_silver,
                                        cost_gold, cost_silver, screen_id, movie_id))
            self.connection.commit()
            print("\n✅ Show added successfully with Show ID:", new_show_id)

        except sql.Error as e:
            print("❌ Error adding show:", e)

    def update_show(self):
        try:
            show_id = input("\nEnter Show ID to update: ")

            print("Leave blank if no change.")
            new_show_time = input("Enter New Show Time (HH:MM:SS): ")
            new_show_date = input("Enter New Show Date (YYYY-MM-DD): ")
            new_seats_gold = input("Enter New Gold Seats Remaining: ")
            new_seats_silver = input("Enter New Silver Seats Remaining: ")
            new_cost_gold = input("Enter New Gold Class Cost: ")
            new_cost_silver = input("Enter New Silver Class Cost: ")
            
            if not self.screen_ids:
                print("🚫 No screens available for this theatre.")
                return
            
            print("\nAvailable Screen IDs:", self.screen_ids)
            new_screen_id = input("Enter New Screen ID: ").upper()

            if new_screen_id not in self.screen_ids:
                print("⚠️ Invalid Screen ID.")
                return

            print("\nAvailable Movie IDs:", self.movie_ids)
            new_movie_id = input("Enter New Movie ID: ")

            if new_movie_id not in self.movie_ids:
                print("⚠️ Invalid Movie ID.")
                return

            update_query = "UPDATE show_table SET "
            update_values = []

            if new_show_time:
                update_query += "Show_Time = %s, "
                update_values.append(new_show_time)

            if new_show_date:
                update_query += "Show_Date = %s, "
                update_values.append(new_show_date)

            if new_seats_gold:
                update_query += "Seats_Remaining_Gold = %s, "
                update_values.append(int(new_seats_gold))

            if new_seats_silver:
                update_query += "Seats_Remaining_Silver = %s, "
                update_values.append(int(new_seats_silver))

            if new_cost_gold:
                update_query += "Class_Cost_Gold = %s, "
                update_values.append(int(new_cost_gold))

            if new_cost_silver:
                update_query += "Class_Cost_Silver = %s, "
                update_values.append(int(new_cost_silver))

            if new_screen_id:
                update_query += "Screen_ID = %s, "
                update_values.append(new_screen_id)

            if new_movie_id:
                update_query += "Movie_ID = %s, "
                update_values.append(new_movie_id)

            update_query = update_query.rstrip(", ")
            update_query += " WHERE Show_ID = %s ;"
            update_values.append(show_id)

            self.cursor.execute(update_query, tuple(update_values))
            self.connection.commit()
            print("\n✅ Show updated successfully.")

        except sql.Error as e:
            print("❌ Error updating show:", e)

    def remove_show(self):
        try:
            show_id = input("\nEnter Show ID to remove: ")
            query = "DELETE FROM show_table WHERE Show_ID = %s ;"
            self.cursor.execute(query, (show_id,))
            self.connection.commit()
            print("\n✅ Show removed successfully.")
        except sql.Error as e:
            print("❌ Error removing show:", e)