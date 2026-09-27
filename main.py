import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import get_connection
from tkcalendar import DateEntry

# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F5F7FA"
HEADER_COLOR = "#0F2A43"
BUTTON_COLOR = "#1D6FA5"
BUTTON_HOVER = "#15547D"
WHITE = "#FFFFFF"
TEXT_COLOR = "#1F2933"
LIGHT_TEXT = "#6B7785"
SUCCESS_COLOR = "#1D8348"
DANGER_COLOR = "#C0392B"
DANGER_HOVER = "#9A2E22"
BORDER_COLOR = "#E1E5EA"


# =========================================================
# ADMIN ACCESS
# =========================================================

ADMIN_PASSWORD = "admin123"


# =========================================================
# USER SESSION
# =========================================================

current_user_id = None
current_user_name = None


# =========================================================
# STYLES
# =========================================================

def setup_styles():

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "TCombobox",
        padding=8,
        font=("Arial", 11)
    )


# =========================================================
# BUTTON HOVER EFFECT
# =========================================================

def add_hover(button, normal_bg, hover_bg):

    button.bind(
        "<Enter>",
        lambda e: button.config(bg=hover_bg)
    )

    button.bind(
        "<Leave>",
        lambda e: button.config(bg=normal_bg)
    )


# =========================================================
# MAIN BUTTON UPDATE
# =========================================================

def update_main_buttons():

    if current_user_id is None:

        my_bookings_button.pack_forget()
        logout_button.pack_forget()
        user_label.pack_forget()

        search_button.pack(pady=10)
        login_button.pack(pady=10)
        register_button.pack(pady=10)

    else:

        login_button.pack_forget()
        register_button.pack_forget()

        search_button.pack(pady=10)
        my_bookings_button.pack(pady=10)
        logout_button.pack(pady=10)

        user_label.config(
            text="Logged in as: " + current_user_name
        )

        user_label.pack(pady=(10, 0))


# =========================================================
# LOGOUT
# =========================================================

def logout_user():

    global current_user_id
    global current_user_name

    current_user_id = None
    current_user_name = None

    update_main_buttons()

    messagebox.showinfo(
        "Logout",
        "You have been logged out."
    )


# =========================================================
# GET STATIONS
# =========================================================

def get_stations():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT station_name
            FROM stations
            ORDER BY station_name
        """)

        stations = [
            row[0]
            for row in cursor.fetchall()
        ]

        return stations

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# REGISTER WINDOW
# =========================================================

def open_register():

    register_window = tk.Toplevel(window)

    register_window.title(
        "Yatrik - Create Account"
    )

    register_window.geometry(
        "520x580"
    )

    register_window.configure(
        bg=BG_COLOR
    )

    # Header
    header = tk.Frame(
        register_window,
        bg=HEADER_COLOR,
        height=90
    )

    header.pack(
        fill="x"
    )

    tk.Frame(
        register_window,
        bg=BUTTON_COLOR,
        height=3
    ).pack(fill="x")

    tk.Label(
        header,
        text="Create Account",
        font=("Arial", 24, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=25)

    form = tk.Frame(
        register_window,
        bg=BG_COLOR
    )

    form.pack(
        pady=25
    )

    # Name
    tk.Label(
        form,
        text="Name",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    name_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=35,
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    name_entry.pack(
        pady=(5, 15)
    )

    # Email
    tk.Label(
        form,
        text="Email",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    email_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=35,
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    email_entry.pack(
        pady=(5, 15)
    )

    # Phone
    tk.Label(
        form,
        text="Phone",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    phone_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=35,
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    phone_entry.pack(
        pady=(5, 15)
    )

    # Password
    tk.Label(
        form,
        text="Password",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    password_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=35,
        show="*",
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    password_entry.pack(
        pady=(5, 20)
    )

    def register_user():

        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        password = password_entry.get()

        if (
            name == ""
            or email == ""
            or phone == ""
            or password == ""
        ):

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO users
                (name, email, phone, password)
                VALUES
                (:1, :2, :3, :4)
            """, (
                name,
                email,
                phone,
                password
            ))

            connection.commit()

            messagebox.showinfo(
                "Registration Successful",
                "Account created successfully!"
            )

            register_window.destroy()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    create_account_button = tk.Button(
        form,
        text="Create Account",
        font=("Arial", 11, "bold"),
        width=25,
        bg=BUTTON_COLOR,
        fg=WHITE,
        activebackground=BUTTON_HOVER,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=register_user
    )

    create_account_button.pack(
        pady=5
    )

    add_hover(create_account_button, BUTTON_COLOR, BUTTON_HOVER)


# =========================================================
# LOGIN WINDOW
# =========================================================

def open_login():

    login_window = tk.Toplevel(window)

    login_window.title(
        "Yatrik - Login"
    )

    login_window.geometry(
        "520x450"
    )

    login_window.configure(
        bg=BG_COLOR
    )

    # Header
    header = tk.Frame(
        login_window,
        bg=HEADER_COLOR,
        height=90
    )

    header.pack(
        fill="x"
    )

    tk.Frame(
        login_window,
        bg=BUTTON_COLOR,
        height=3
    ).pack(fill="x")

    tk.Label(
        header,
        text="Login to Yatrik",
        font=("Arial", 24, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=25)

    form = tk.Frame(
        login_window,
        bg=BG_COLOR
    )

    form.pack(
        pady=35
    )

    # Email
    tk.Label(
        form,
        text="Email",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    email_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=35,
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    email_entry.pack(
        pady=(5, 20)
    )

    # Password
    tk.Label(
        form,
        text="Password",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    password_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=35,
        show="*",
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    password_entry.pack(
        pady=(5, 25)
    )

    def login_user():

        global current_user_id
        global current_user_name

        email = email_entry.get().strip()
        password = password_entry.get()

        if email == "" or password == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter email and password."
            )

            return

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT user_id, name
                FROM users
                WHERE email = :1
                AND password = :2
            """, (
                email,
                password
            ))

            user = cursor.fetchone()

            if user:

                current_user_id = user[0]
                current_user_name = user[1]

                update_main_buttons()

                messagebox.showinfo(
                    "Login Successful",
                    "Welcome " + current_user_name
                )

                login_window.destroy()

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid email or password."
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    login_submit_button = tk.Button(
        form,
        text="Login",
        font=("Arial", 11, "bold"),
        width=25,
        bg=BUTTON_COLOR,
        fg=WHITE,
        activebackground=BUTTON_HOVER,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=login_user
    )

    login_submit_button.pack()

    add_hover(login_submit_button, BUTTON_COLOR, BUTTON_HOVER)


# =========================================================
# BOOKING WINDOW
# =========================================================

def open_booking(train):

    if current_user_id is None:

        messagebox.showwarning(
            "Login Required",
            "Please login before booking a ticket."
        )

        return

    booking_window = tk.Toplevel(window)

    booking_window.title(
        "Yatrik - Book Ticket"
    )

    booking_window.geometry(
        "560x720"
    )

    booking_window.configure(
        bg=BG_COLOR
    )

    # Header
    header = tk.Frame(
        booking_window,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Frame(
        booking_window,
        bg=BUTTON_COLOR,
        height=3
    ).pack(fill="x")

    tk.Label(
        header,
        text="Book Ticket",
        font=("Arial", 24, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=18)

    tk.Label(
        header,
        text=train[2],
        font=("Arial", 14, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(
        pady=(0, 15)
    )

    form = tk.Frame(
        booking_window,
        bg=BG_COLOR
    )

    form.pack(
        pady=20
    )

    # Train number
    tk.Label(
        form,
        text="Train No: " + str(train[1]),
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 15)
    )

    # Passenger Name
    tk.Label(
        form,
        text="Passenger Name",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    passenger_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=35,
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    passenger_entry.pack(
        pady=(5, 15)
    )

    # Age
    tk.Label(
        form,
        text="Age",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    age_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=35,
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    age_entry.pack(
        pady=(5, 15)
    )

    # Gender
    tk.Label(
        form,
        text="Gender",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    gender_var = tk.StringVar(
        value="Male"
    )

    gender_dropdown = ttk.Combobox(
        form,
        textvariable=gender_var,
        values=[
            "Male",
            "Female",
            "Other"
        ],
        state="readonly",
        width=33
    )

    gender_dropdown.pack(
        pady=(5, 15)
    )

        # Journey Date
    tk.Label(
        form,
        text="Journey Date",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    date_entry = DateEntry(
        form,
        width=32,
        font=("Arial", 11),
        date_pattern="yyyy-mm-dd",
        background=BUTTON_COLOR,
        foreground=WHITE,
        borderwidth=1,
        relief="solid",
        mindate=datetime.now().date()
    )

    date_entry.pack(
        pady=(5, 20)
    )

    def book_ticket():

        passenger_name = passenger_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_var.get()
        journey_date = date_entry.get().strip()

        if (
            passenger_name == ""
            or age == ""
            or journey_date == ""
        ):

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        try:
            age = int(age)

            if age <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Information",
                "Please enter a valid age."
            )

            return

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT available_seats
                FROM trains
                WHERE train_id = :1
            """, (
                train[0],
            ))

            seats = cursor.fetchone()

            if seats is None:

                messagebox.showerror(
                    "Error",
                    "Train not found."
                )

                return

            if seats[0] <= 0:

                messagebox.showwarning(
                    "No Seats",
                    "No seats are available."
                )

                return

            pnr = (
                "YAT"
                + datetime.now().strftime(
                    "%d%m%y%H%M%S"
                )
            )

            cursor.execute("""
                INSERT INTO bookings
                (
                    user_id,
                    train_id,
                    passenger_name,
                    age,
                    gender,
                    journey_date,
                    pnr,
                    status
                )
                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    :5,
                    TO_DATE(:6, 'YYYY-MM-DD'),
                    :7,
                    'CONFIRMED'
                )
            """, (
                current_user_id,
                train[0],
                passenger_name,
                age,
                gender,
                journey_date,
                pnr
            ))

            cursor.execute("""
                UPDATE trains
                SET available_seats =
                    available_seats - 1
                WHERE train_id = :1
            """, (
                train[0],
            ))

            connection.commit()

            messagebox.showinfo(
                "Booking Successful",
                "Ticket booked successfully!\n\n"
                "PNR: " + pnr
            )

            booking_window.destroy()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    confirm_booking_button = tk.Button(
        form,
        text="Confirm Booking",
        font=("Arial", 11, "bold"),
        width=25,
        bg=BUTTON_COLOR,
        fg=WHITE,
        activebackground=BUTTON_HOVER,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=book_ticket
    )

    confirm_booking_button.pack(
        pady=5
    )

    add_hover(confirm_booking_button, BUTTON_COLOR, BUTTON_HOVER)
# =========================================================
# SEARCH TRAINS WINDOW
# =========================================================

def open_search():

    search_window = tk.Toplevel(window)

    search_window.title(
        "Yatrik - Search Trains"
    )

    search_window.geometry(
        "850x700"
    )

    search_window.configure(
        bg=BG_COLOR
    )

    # Header
    header = tk.Frame(
        search_window,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Frame(
        search_window,
        bg=BUTTON_COLOR,
        height=3
    ).pack(fill="x")

    tk.Label(
        header,
        text="Search Trains",
        font=("Arial", 24, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=20)

    # Search area
    search_frame = tk.Frame(
        search_window,
        bg=BG_COLOR
    )

    search_frame.pack(
        pady=20
    )

    tk.Label(
        search_frame,
        text="From",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=5
    )

    tk.Label(
        search_frame,
        text="To",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=5
    )

    stations = get_stations()

    if not stations:

        search_window.destroy()
        return

    from_var = tk.StringVar()
    to_var = tk.StringVar()

    from_dropdown = ttk.Combobox(
        search_frame,
        textvariable=from_var,
        values=stations,
        state="readonly",
        width=25
    )

    from_dropdown.grid(
        row=1,
        column=0,
        padx=10
    )

    to_dropdown = ttk.Combobox(
        search_frame,
        textvariable=to_var,
        values=stations,
        state="readonly",
        width=25
    )

    to_dropdown.grid(
        row=1,
        column=1,
        padx=10
    )

    # Results
    # ---------------- SCROLLABLE TRAIN LIST ----------------

    results_container = tk.Frame(
        search_window,
        bg=BG_COLOR
    )

    results_container.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    canvas = tk.Canvas(
        results_container,
        bg=BG_COLOR,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        results_container,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    results_frame = tk.Frame(
        canvas,
        bg=BG_COLOR
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=results_frame,
        anchor="nw"
    )


    def update_scroll_region(event=None):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )


    def resize_canvas_window(event):
        canvas.itemconfig(
            canvas_window,
            width=event.width
        )


    results_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        resize_canvas_window
    )


    def mouse_wheel(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    canvas.bind_all(
        "<MouseWheel>",
        mouse_wheel
    )

    def search_trains():

        source = from_var.get()
        destination = to_var.get()

        if source == "" or destination == "":

            messagebox.showwarning(
                "Missing Information",
                "Please select both stations."
            )

            return

        if source == destination:

            messagebox.showwarning(
                "Invalid Search",
                "Source and destination cannot be the same."
            )

            return

        for widget in results_frame.winfo_children():
            widget.destroy()

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    train_id,
                    train_number,
                    train_name,
                    departure_time,
                    arrival_time,
                    fare,
                    available_seats
                FROM trains
                WHERE source = :1
                AND destination = :2
            """, (
                source,
                destination
            ))

            trains = cursor.fetchall()

            if not trains:

                tk.Label(
                    results_frame,
                    text="No trains found.",
                    font=("Arial", 14),
                    bg=BG_COLOR,
                    fg=LIGHT_TEXT
                ).pack(
                    pady=30
                )

                return

            for train in trains:

                train_card = tk.Frame(
                    results_frame,
                    bg=WHITE,
                    relief="flat",
                    bd=0,
                    highlightbackground=BORDER_COLOR,
                    highlightthickness=1
                )

                train_card.pack(
                    fill="x",
                    pady=8
                )

                tk.Label(
                    train_card,
                    text=train[2],
                    font=("Arial", 15, "bold"),
                    bg=WHITE,
                    fg=HEADER_COLOR
                ).pack(
                    pady=(12, 4)
                )

                tk.Label(
                    train_card,
                    text="Train No: " + str(train[1]),
                    font=("Arial", 10),
                    bg=WHITE,
                    fg=LIGHT_TEXT
                ).pack()

                tk.Label(
                    train_card,
                    text=(
                        str(train[3])
                        + "  →  "
                        + str(train[4])
                    ),
                    font=("Arial", 11, "bold"),
                    bg=WHITE,
                    fg=TEXT_COLOR
                ).pack(
                    pady=5
                )

                tk.Label(
                    train_card,
                    text=(
                        "Fare: ₹"
                        + str(train[5])
                        + "     "
                        + "Available Seats: "
                        + str(train[6])
                    ),
                    font=("Arial", 10),
                    bg=WHITE,
                    fg=TEXT_COLOR
                ).pack()

                book_ticket_button = tk.Button(
                    train_card,
                    text="Book Ticket",
                    font=("Arial", 10, "bold"),
                    width=18,
                    bg=BUTTON_COLOR,
                    fg=WHITE,
                    activebackground=BUTTON_HOVER,
                    activeforeground=WHITE,
                    relief="flat",
                    cursor="hand2",
                    command=lambda t=train:
                    open_booking(t)
                )

                book_ticket_button.pack(
                    pady=12
                )

                add_hover(book_ticket_button, BUTTON_COLOR, BUTTON_HOVER)

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    search_submit_button = tk.Button(
        search_frame,
        text="Search",
        font=("Arial", 11, "bold"),
        width=18,
        bg=BUTTON_COLOR,
        fg=WHITE,
        activebackground=BUTTON_HOVER,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=search_trains
    )

    search_submit_button.grid(
        row=2,
        column=0,
        columnspan=2,
        pady=18
    )

    add_hover(search_submit_button, BUTTON_COLOR, BUTTON_HOVER)


# =========================================================
# MY BOOKINGS WINDOW
# =========================================================

def open_my_bookings():

    if current_user_id is None:

        messagebox.showwarning(
            "Login Required",
            "Please login to view your bookings."
        )

        return

    bookings_window = tk.Toplevel(window)

    bookings_window.title(
        "Yatrik - My Bookings"
    )

    bookings_window.geometry(
        "900x700"
    )

    bookings_window.configure(
        bg=BG_COLOR
    )

    # Header
    header = tk.Frame(
        bookings_window,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Frame(
        bookings_window,
        bg=BUTTON_COLOR,
        height=3
    ).pack(fill="x")

    tk.Label(
        header,
        text="My Bookings",
        font=("Arial", 24, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=20)

    # ---------------- SCROLLABLE BOOKINGS LIST ----------------

    results_container = tk.Frame(
        bookings_window,
        bg=BG_COLOR
    )

    results_container.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    canvas = tk.Canvas(
        results_container,
        bg=BG_COLOR,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        results_container,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    results_frame = tk.Frame(
        canvas,
        bg=BG_COLOR
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=results_frame,
        anchor="nw"
    )

    def update_scroll_region(event=None):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    def resize_canvas_window(event):
        canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    results_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        resize_canvas_window
    )

    def mouse_wheel(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mouse_wheel
    )

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                b.booking_id,
                b.passenger_name,
                t.train_name,
                t.source,
                t.destination,
                b.journey_date,
                b.pnr,
                b.status,
                b.train_id
            FROM bookings b
            JOIN trains t
            ON b.train_id = t.train_id
            WHERE b.user_id = :1
            ORDER BY b.booking_id
        """, (
            current_user_id,
        ))

        bookings = cursor.fetchall()

        if not bookings:

            tk.Label(
                results_frame,
                text="No bookings found.",
                font=("Arial", 14),
                bg=BG_COLOR,
                fg=LIGHT_TEXT
            ).pack(
                pady=40
            )

            return

        for booking in bookings:

            booking_id = booking[0]
            passenger_name = booking[1]
            train_name = booking[2]
            source = booking[3]
            destination = booking[4]
            journey_date = booking[5]
            pnr = booking[6]
            status = booking[7]
            train_id = booking[8]

            booking_card = tk.Frame(
                results_frame,
                bg=WHITE,
                relief="flat",
                bd=0,
                highlightbackground=BORDER_COLOR,
                highlightthickness=1
            )

            booking_card.pack(
                fill="x",
                pady=8
            )

            tk.Label(
                booking_card,
                text="Booking ID: " + str(booking_id),
                font=("Arial", 10, "bold"),
                bg=WHITE,
                fg=LIGHT_TEXT
            ).pack(
                pady=(12, 3)
            )

            tk.Label(
                booking_card,
                text=train_name,
                font=("Arial", 15, "bold"),
                bg=WHITE,
                fg=HEADER_COLOR
            ).pack()

            tk.Label(
                booking_card,
                text=(
                    str(source)
                    + "  →  "
                    + str(destination)
                ),
                font=("Arial", 11),
                bg=WHITE,
                fg=TEXT_COLOR
            ).pack(
                pady=4
            )

            tk.Label(
                booking_card,
                text="Passenger: " + str(passenger_name),
                font=("Arial", 11),
                bg=WHITE,
                fg=TEXT_COLOR
            ).pack()

            formatted_date = journey_date.strftime(
                "%d-%b-%Y"
            )

            tk.Label(
                booking_card,
                text="Journey Date: " + formatted_date,
                font=("Arial", 11),
                bg=WHITE,
                fg=TEXT_COLOR
            ).pack(
                pady=3
            )

            tk.Label(
                booking_card,
                text="PNR: " + str(pnr),
                font=("Arial", 11, "bold"),
                bg=WHITE,
                fg=TEXT_COLOR
            ).pack()

            status_color = (
                SUCCESS_COLOR
                if status == "CONFIRMED"
                else DANGER_COLOR
            )

            tk.Label(
                booking_card,
                text="Status: " + str(status),
                font=("Arial", 11, "bold"),
                bg=WHITE,
                fg=status_color
            ).pack(
                pady=5
            )

            if status == "CONFIRMED":

                cancel_booking_button = tk.Button(
                    booking_card,
                    text="Cancel Booking",
                    font=("Arial", 10, "bold"),
                    width=18,
                    bg=DANGER_COLOR,
                    fg=WHITE,
                    activebackground=DANGER_HOVER,
                    activeforeground=WHITE,
                    relief="flat",
                    cursor="hand2",
                    command=lambda b_id=booking_id,
                                   t_id=train_id:
                    cancel_booking(
                        b_id,
                        t_id,
                        bookings_window
                    )
                )

                cancel_booking_button.pack(
                    pady=(5, 15)
                )

                add_hover(cancel_booking_button, DANGER_COLOR, DANGER_HOVER)

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# CANCEL BOOKING
# =========================================================

def cancel_booking(
    booking_id,
    train_id,
    bookings_window
):

    answer = messagebox.askyesno(
        "Cancel Booking",
        "Are you sure you want to cancel this booking?"
    )

    if not answer:
        return

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT status
            FROM bookings
            WHERE booking_id = :1
            AND user_id = :2
        """, (
            booking_id,
            current_user_id
        ))

        booking = cursor.fetchone()

        if booking is None:

            messagebox.showerror(
                "Error",
                "Booking not found."
            )

            return

        if booking[0] == "CANCELLED":

            messagebox.showinfo(
                "Already Cancelled",
                "This booking is already cancelled."
            )

            return

        cursor.execute("""
            UPDATE bookings
            SET status = 'CANCELLED'
            WHERE booking_id = :1
            AND user_id = :2
        """, (
            booking_id,
            current_user_id
        ))

        cursor.execute("""
            UPDATE trains
            SET available_seats =
                available_seats + 1
            WHERE train_id = :1
        """, (
            train_id,
        ))

        connection.commit()

        messagebox.showinfo(
            "Cancellation Successful",
            "Booking cancelled successfully."
        )

        bookings_window.destroy()

        open_my_bookings()

    except Exception as e:

        if connection:
            connection.rollback()

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# ADMIN LOGIN WINDOW
# =========================================================

def open_admin_login():

    admin_window = tk.Toplevel(window)

    admin_window.title(
        "Yatrik - Admin Login"
    )

    admin_window.geometry(
        "420x300"
    )

    admin_window.configure(
        bg=BG_COLOR
    )

    header = tk.Frame(
        admin_window,
        bg=HEADER_COLOR,
        height=90
    )

    header.pack(
        fill="x"
    )

    tk.Frame(
        admin_window,
        bg=BUTTON_COLOR,
        height=3
    ).pack(fill="x")

    tk.Label(
        header,
        text="Admin Login",
        font=("Arial", 22, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=25)

    form = tk.Frame(
        admin_window,
        bg=BG_COLOR
    )

    form.pack(
        pady=30
    )

    tk.Label(
        form,
        text="Admin Password",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    password_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=30,
        show="*",
        relief="flat",
        bd=0,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    password_entry.pack(
        pady=(5, 20)
    )

    def verify_admin():

        entered_password = password_entry.get()

        if entered_password == ADMIN_PASSWORD:

            admin_window.destroy()
            open_manage_trains()

        else:

            messagebox.showerror(
                "Access Denied",
                "Incorrect admin password."
            )

    admin_submit_button = tk.Button(
        form,
        text="Login",
        font=("Arial", 11, "bold"),
        width=22,
        bg=BUTTON_COLOR,
        fg=WHITE,
        activebackground=BUTTON_HOVER,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=verify_admin
    )

    admin_submit_button.pack()

    add_hover(admin_submit_button, BUTTON_COLOR, BUTTON_HOVER)


# =========================================================
# MANAGE TRAINS WINDOW
# =========================================================

def open_manage_trains():

    manage_window = tk.Toplevel(window)

    manage_window.title(
        "Yatrik - Manage Trains"
    )

    manage_window.geometry(
        "850x700"
    )

    manage_window.configure(
        bg=BG_COLOR
    )

    header = tk.Frame(
        manage_window,
        bg=HEADER_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Frame(
        manage_window,
        bg=BUTTON_COLOR,
        height=3
    ).pack(fill="x")

    tk.Label(
        header,
        text="Manage Trains",
        font=("Arial", 24, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=20)

    top_bar = tk.Frame(
        manage_window,
        bg=BG_COLOR
    )

    top_bar.pack(
        pady=15
    )

    add_train_button = tk.Button(
        top_bar,
        text="Add Train",
        font=("Arial", 11, "bold"),
        width=20,
        bg=BUTTON_COLOR,
        fg=WHITE,
        activebackground=BUTTON_HOVER,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=lambda: open_train_form(manage_window, None)
    )

    add_train_button.pack()

    add_hover(add_train_button, BUTTON_COLOR, BUTTON_HOVER)

    # ---------------- SCROLLABLE TRAIN LIST ----------------

    results_container = tk.Frame(
        manage_window,
        bg=BG_COLOR
    )

    results_container.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    canvas = tk.Canvas(
        results_container,
        bg=BG_COLOR,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        results_container,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    results_frame = tk.Frame(
        canvas,
        bg=BG_COLOR
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=results_frame,
        anchor="nw"
    )

    def update_scroll_region(event=None):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    def resize_canvas_window(event):
        canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    results_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        resize_canvas_window
    )

    def mouse_wheel(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mouse_wheel
    )

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                train_id,
                train_number,
                train_name,
                source,
                destination,
                departure_time,
                arrival_time,
                fare,
                available_seats
            FROM trains
            ORDER BY train_name
        """)

        trains = cursor.fetchall()

        if not trains:

            tk.Label(
                results_frame,
                text="No trains found.",
                font=("Arial", 14),
                bg=BG_COLOR,
                fg=LIGHT_TEXT
            ).pack(
                pady=30
            )

            return

        for train in trains:

            train_card = tk.Frame(
                results_frame,
                bg=WHITE,
                relief="flat",
                bd=0,
                highlightbackground=BORDER_COLOR,
                highlightthickness=1
            )

            train_card.pack(
                fill="x",
                pady=8
            )

            tk.Label(
                train_card,
                text=train[2],
                font=("Arial", 15, "bold"),
                bg=WHITE,
                fg=HEADER_COLOR
            ).pack(
                pady=(12, 4)
            )

            tk.Label(
                train_card,
                text="Train No: " + str(train[1]),
                font=("Arial", 10),
                bg=WHITE,
                fg=LIGHT_TEXT
            ).pack()

            tk.Label(
                train_card,
                text=(
                    str(train[3])
                    + "  →  "
                    + str(train[4])
                ),
                font=("Arial", 11, "bold"),
                bg=WHITE,
                fg=TEXT_COLOR
            ).pack(
                pady=5
            )

            tk.Label(
                train_card,
                text=(
                    str(train[5])
                    + "  -  "
                    + str(train[6])
                ),
                font=("Arial", 10),
                bg=WHITE,
                fg=TEXT_COLOR
            ).pack()

            tk.Label(
                train_card,
                text=(
                    "Fare: ₹"
                    + str(train[7])
                    + "     "
                    + "Available Seats: "
                    + str(train[8])
                ),
                font=("Arial", 10),
                bg=WHITE,
                fg=TEXT_COLOR
            ).pack(
                pady=(3, 10)
            )

            button_row = tk.Frame(
                train_card,
                bg=WHITE
            )

            button_row.pack(
                pady=(0, 12)
            )

            edit_button = tk.Button(
                button_row,
                text="Edit",
                font=("Arial", 10, "bold"),
                width=12,
                bg=BUTTON_COLOR,
                fg=WHITE,
                activebackground=BUTTON_HOVER,
                activeforeground=WHITE,
                relief="flat",
                cursor="hand2",
                command=lambda t=train:
                open_train_form(manage_window, t)
            )

            edit_button.pack(
                side="left",
                padx=5
            )

            add_hover(edit_button, BUTTON_COLOR, BUTTON_HOVER)

            delete_button = tk.Button(
                button_row,
                text="Delete",
                font=("Arial", 10, "bold"),
                width=12,
                bg=DANGER_COLOR,
                fg=WHITE,
                activebackground=DANGER_HOVER,
                activeforeground=WHITE,
                relief="flat",
                cursor="hand2",
                command=lambda t_id=train[0]:
                delete_train(t_id, manage_window)
            )

            delete_button.pack(
                side="left",
                padx=5
            )

            add_hover(delete_button, DANGER_COLOR, DANGER_HOVER)

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# ADD / EDIT TRAIN FORM
# =========================================================

def open_train_form(manage_window, train):

    is_edit = train is not None

    form_window = tk.Toplevel(window)

    form_window.title(
        "Yatrik - Edit Train" if is_edit else "Yatrik - Add Train"
    )

    form_window.geometry(
        "520x680"
    )

    form_window.configure(
        bg=BG_COLOR
    )

    header = tk.Frame(
        form_window,
        bg=HEADER_COLOR,
        height=90
    )

    header.pack(
        fill="x"
    )

    tk.Frame(
        form_window,
        bg=BUTTON_COLOR,
        height=3
    ).pack(fill="x")

    tk.Label(
        header,
        text="Edit Train" if is_edit else "Add Train",
        font=("Arial", 22, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=25)

    form = tk.Frame(
        form_window,
        bg=BG_COLOR
    )

    form.pack(
        pady=20
    )

    def add_field(label_text):

        tk.Label(
            form,
            text=label_text,
            font=("Arial", 11, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w"
        )

        entry = tk.Entry(
            form,
            font=("Arial", 11),
            width=35,
            relief="flat",
            bd=0,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        entry.pack(
            pady=(5, 12)
        )

        return entry

    train_number_entry = add_field("Train Number")
    train_name_entry = add_field("Train Name")
    source_entry = add_field("Source")
    destination_entry = add_field("Destination")
    departure_entry = add_field("Departure Time (HH:MM)")
    arrival_entry = add_field("Arrival Time (HH:MM)")
    fare_entry = add_field("Fare")
    seats_entry = add_field("Available Seats")

    if is_edit:

        train_number_entry.insert(0, str(train[1]))
        train_name_entry.insert(0, str(train[2]))
        source_entry.insert(0, str(train[3]))
        destination_entry.insert(0, str(train[4]))
        departure_entry.insert(0, str(train[5]))
        arrival_entry.insert(0, str(train[6]))
        fare_entry.insert(0, str(train[7]))
        seats_entry.insert(0, str(train[8]))

    def save_train():

        train_number = train_number_entry.get().strip()
        train_name = train_name_entry.get().strip()
        source = source_entry.get().strip()
        destination = destination_entry.get().strip()
        departure_time = departure_entry.get().strip()
        arrival_time = arrival_entry.get().strip()
        fare = fare_entry.get().strip()
        available_seats = seats_entry.get().strip()

        if (
            train_number == ""
            or train_name == ""
            or source == ""
            or destination == ""
            or departure_time == ""
            or arrival_time == ""
            or fare == ""
            or available_seats == ""
        ):

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        try:

            fare = float(fare)
            available_seats = int(available_seats)

            if fare <= 0 or available_seats < 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Information",
                "Please enter a valid fare and seat count."
            )

            return

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if is_edit:

                cursor.execute("""
                    UPDATE trains
                    SET
                        train_number = :1,
                        train_name = :2,
                        source = :3,
                        destination = :4,
                        departure_time = :5,
                        arrival_time = :6,
                        fare = :7,
                        available_seats = :8
                    WHERE train_id = :9
                """, (
                    train_number,
                    train_name,
                    source,
                    destination,
                    departure_time,
                    arrival_time,
                    fare,
                    available_seats,
                    train[0]
                ))

            else:

                cursor.execute("""
                    INSERT INTO trains
                    (
                        train_number,
                        train_name,
                        source,
                        destination,
                        departure_time,
                        arrival_time,
                        fare,
                        available_seats
                    )
                    VALUES
                    (
                        :1, :2, :3, :4, :5, :6, :7, :8
                    )
                """, (
                    train_number,
                    train_name,
                    source,
                    destination,
                    departure_time,
                    arrival_time,
                    fare,
                    available_seats
                ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Train updated successfully!" if is_edit
                else "Train added successfully!"
            )

            form_window.destroy()
            manage_window.destroy()
            open_manage_trains()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    save_train_button = tk.Button(
        form,
        text="Save Train",
        font=("Arial", 11, "bold"),
        width=25,
        bg=BUTTON_COLOR,
        fg=WHITE,
        activebackground=BUTTON_HOVER,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=save_train
    )

    save_train_button.pack(
        pady=10
    )

    add_hover(save_train_button, BUTTON_COLOR, BUTTON_HOVER)


# =========================================================
# DELETE TRAIN
# =========================================================

def delete_train(train_id, manage_window):

    answer = messagebox.askyesno(
        "Delete Train",
        "Are you sure you want to delete this train?"
    )

    if not answer:
        return

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM bookings
            WHERE train_id = :1
        """, (
            train_id,
        ))

        booking_count = cursor.fetchone()[0]

        if booking_count > 0:

            messagebox.showwarning(
                "Cannot Delete",
                "This train has "
                + str(booking_count)
                + " booking(s) linked to it.\n"
                "Cancel or remove those bookings first."
            )

            return

        cursor.execute("""
            DELETE FROM trains
            WHERE train_id = :1
        """, (
            train_id,
        ))

        connection.commit()

        messagebox.showinfo(
            "Deleted",
            "Train deleted successfully."
        )

        manage_window.destroy()
        open_manage_trains()

    except Exception as e:

        if connection:
            connection.rollback()

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title(
    "Yatrik - Railway Reservation System"
)

window.geometry(
    "900x650"
)

window.configure(
    bg=BG_COLOR
)

setup_styles()


# ---------------- HEADER ----------------

header = tk.Frame(
    window,
    bg=HEADER_COLOR
)

header.pack(
    fill="x"
)

tk.Frame(
    window,
    bg=BUTTON_COLOR,
    height=3
).pack(fill="x")

tk.Label(
    header,
    text="YATRIK",
    font=("Arial", 32, "bold"),
    bg=HEADER_COLOR,
    fg=WHITE
).pack(
    pady=(30, 5)
)

tk.Label(
    header,
    text="Railway Reservation System",
    font=("Arial", 13),
    bg=HEADER_COLOR,
    fg="#D9E4EC"
).pack(
    pady=(0, 25)
)


# ---------------- CONTENT ----------------

content = tk.Frame(
    window,
    bg=BG_COLOR
)

content.pack(
    expand=True
)


tk.Label(
    content,
    text="Welcome to Yatrik",
    font=("Arial", 18, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    pady=(35, 5)
)

tk.Label(
    content,
    text="Search trains, book tickets and manage your bookings",
    font=("Arial", 10),
    bg=BG_COLOR,
    fg=LIGHT_TEXT
).pack(
    pady=(0, 15)
)


# ---------------- USER LABEL ----------------

user_label = tk.Label(
    content,
    text="",
    font=("Arial", 10, "bold"),
    bg=BG_COLOR,
    fg=SUCCESS_COLOR
)


# ---------------- BUTTONS ----------------

search_button = tk.Button(
    content,
    text="Search Trains",
    font=("Arial", 11, "bold"),
    width=25,
    height=1,
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=BUTTON_HOVER,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=open_search
)

add_hover(search_button, BUTTON_COLOR, BUTTON_HOVER)


my_bookings_button = tk.Button(
    content,
    text="My Bookings",
    font=("Arial", 11, "bold"),
    width=25,
    height=1,
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=BUTTON_HOVER,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=open_my_bookings
)

add_hover(my_bookings_button, BUTTON_COLOR, BUTTON_HOVER)


login_button = tk.Button(
    content,
    text="Login",
    font=("Arial", 11, "bold"),
    width=25,
    height=1,
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=BUTTON_HOVER,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=open_login
)

add_hover(login_button, BUTTON_COLOR, BUTTON_HOVER)


register_button = tk.Button(
    content,
    text="Register",
    font=("Arial", 11, "bold"),
    width=25,
    height=1,
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=BUTTON_HOVER,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=open_register
)

add_hover(register_button, BUTTON_COLOR, BUTTON_HOVER)


logout_button = tk.Button(
    content,
    text="Logout",
    font=("Arial", 11, "bold"),
    width=25,
    height=1,
    bg=DANGER_COLOR,
    fg=WHITE,
    activebackground="#A61B1B",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=logout_user
)

add_hover(logout_button, DANGER_COLOR, DANGER_HOVER)


admin_login_button = tk.Button(
    content,
    text="Admin Login",
    font=("Arial", 9, "underline"),
    bg=BG_COLOR,
    fg=LIGHT_TEXT,
    activeforeground=BUTTON_COLOR,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=open_admin_login
)

admin_login_button.pack(
    pady=(20, 10)
)


# ---------------- START ----------------

update_main_buttons()

window.mainloop()