from .admin_base import AdminBase
import mysql.connector as sql
from rich.console import Console
from rich.table import Table
# movie table
class ManageMovie(AdminBase):

    def __init__(self):
        super().__init__()
        self.movie_menu()

    def movie_menu(self):
        while True:
            print("\n\t\t----🎬  Show Management - Theatre ID: ----")
            print("\t\t\t1. Add Movie")
            print("\t\t\t2. Remove Movie")
            print("\t\t\t3. Update Movie")
            print("\t\t\t4. View Movies")
            print("\t\t\t5. Exit")
            choice = input("👉 Enter your choice: ")

            if choice == '1':
                self.add_movie()
            elif choice == '2':
                self.remove_movie()
            elif choice == '3':
                self.update_movie()
            elif choice == '4':
                self.view_movies()
            elif choice == '5':
                break
            else:
                print("⚠️ Invalid choice, please try again.")

    def add_movie(self):
        try:
            print("\n📝 Add New Movie")

            name = input("Enter Movie Name: ")
            language = input("Enter Language: ")
            genre = input("Enter Genre: ")

            target_audience_dict = {
                'U': 'Universal',
                'U/A': 'Parental Guidance',
                'A': 'Adult',
                'PG': 'Parental Guidance',
                'R': 'Restricted',
                'NC-17': 'No One Under 17 Admitted'
            }

            print("\nTarget Audience Options:")
            for key, value in target_audience_dict.items():
                print(f"{key}: {value}")

            target_audience = input("\nEnter Target Audience (U, U/A, A, PG, R, NC-17): ").upper()

            if target_audience not in target_audience_dict:
                print("⚠️ Invalid Target Audience.")
                return

            query = """
                SELECT Movie_ID FROM movie ORDER BY Movie_ID DESC LIMIT 1;
            """
            self.cursor.execute(query)
            result = self.cursor.fetchone()

            if result:
                last_movie_id = result[0]
                new_number = str(int(last_movie_id) + 1).zfill(3)
                # zfill ->use for 3 digit means first two 0 001,..011
            else:
                new_number = "001"

            new_movie_id = new_number

            query = """
                INSERT INTO movie (Movie_ID, Name, Language, Genre, Target_Audience)
                VALUES (%s, %s, %s, %s, %s);
            """
            self.cursor.execute(query, (new_movie_id, name, language, genre, target_audience))
            self.connection.commit()
            print("\n✅ Movie added successfully with Movie ID:", new_movie_id)

        except sql.Error as e:
            print("❌ Error adding movie:", e)


    def remove_movie(self):
        try:
            movie_id = input("\nEnter Movie ID to remove: ")

            query = "DELETE FROM movie WHERE Movie_ID = %s;"
            self.cursor.execute(query, (movie_id,))
            self.connection.commit()

            print("\n✅ Movie removed successfully.")
        except sql.Error as e:
            print("❌ Error removing movie:", e)

    def update_movie(self):
        try:
            movie_id = input("\nEnter Movie ID to update: ")

            print("Leave blank if no change.")
            new_name = input("Enter New Movie Name: ")
            new_language = input("Enter New Language: ")
            new_genre = input("Enter New Genre: ")

            target_audience_dict = {
                'U': 'Universal',
                'U/A': 'Parental Guidance',
                'A': 'Adult',
                'PG': 'Parental Guidance',
                'R': 'Restricted',
                'NC-17': 'No One Under 17 Admitted'
            }

            print("\nTarget Audience Options:")
            for key, value in target_audience_dict.items():
                print(f"{key}: {value}")

            new_target_audience = input("\nEnter New Target Audience (U, U/A, A, PG, R, NC-17): ").upper()

            if new_target_audience and new_target_audience not in target_audience_dict:
                print("⚠️ Invalid Target Audience.")
                return

            update_query = "UPDATE movie SET "
            update_values = []

            if new_name:
                update_query += "Name = %s, "
                update_values.append(new_name)

            if new_language:
                update_query += "Language = %s, "
                update_values.append(new_language)

            if new_genre:
                update_query += "Genre = %s, "
                update_values.append(new_genre)

            if new_target_audience:
                update_query += "Target_Audience = %s, "
                update_values.append(new_target_audience)

            update_query = update_query.rstrip(", ")
            update_query += " WHERE Movie_ID = %s;"
            update_values.append(movie_id)

            self.cursor.execute(update_query, tuple(update_values))
            self.connection.commit()

            print("\n✅ Movie updated successfully.")

        except sql.Error as e:
            print("❌ Error updating movie:", e)

    def view_movies(self):
        try:
            query = """
                SELECT Movie_ID, Name, Language, Genre, Target_Audience
                FROM movie;
            """
            self.cursor.execute(query)
            movies = self.cursor.fetchall()

            if not movies:
                print("🚫 No movies found.")
                return

            console = Console()

            
            table = Table(title="🎬 Movies List", show_lines=True)

            # Define table columns
            table.add_column("Movie ID", justify="center", style="cyan")
            table.add_column("Name", justify="left", style="blue", no_wrap=True)
            table.add_column("Language", justify="center", style="green")
            table.add_column("Genre", justify="center", style="magenta")
            table.add_column("Target Audience", justify="center", style="yellow")

            # Add rows to the table
            for movie in movies:
                table.add_row(
                    str(movie[0]),  # Movie ID
                    movie[1],       # Name
                    movie[2],       # Language
                    movie[3],       # Genre
                    movie[4]        # Target Audience
                )

            
            console.print(table)

        except sql.Error as e:
            print("❌ Error fetching movies:", e)