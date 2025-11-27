import datetime
import random

# SAMPLE BOOK DATA (20 books)
sample_titles = [
    "Shadows of the Valley", "Echoes of the Horizon", "Waves of Destiny",
    "Silent Moon", "Broken Compass", "Forest of Whispers", "Golden Sands",
    "The Last Ember", "Stormbound", "Crimson Voyage", "Fading Stars",
    "The Hidden Path", "Nightfall Requiem", "Frozen Memories",
    "Ironbound Oath", "Winds of Tomorrow", "Fallen Kingdom",
    "The Lost Lantern", "Dreams of Solitude", "Eternal Voyage"
]

sample_authors = [
    "A. Santos", "J. Dela Cruz", "M. Reyes", "K. Villanueva", "P. Mendoza",
    "R. Navarro", "S. Ocampo", "E. Ramirez", "T. Soriano", "L. Vergara",
    "C. Basilio", "G. Tan", "H. Uy", "V. Carreon", "N. Flores",
    "D. Robles", "F. Bautista", "J. Ortega", "M. Salazar", "R. Aquino"
]

books = []
for i in range(20):
    books.append({
        "id": f"B{i+1:03d}",
        "title": sample_titles[i],
        "author": random.choice(sample_authors),
        "available": True
    })

# -----------------------------
# Application state storage
# -----------------------------
active_borrows = []   # current borrow records (not returned)
history = []          # all transactions (borrow + return) chronological (append order)

# -----------------------------
# Custom fine / escalation policy (Option 3 chosen)
# -----------------------------
FINE_PER_DAY = 5          # pesos per overdue day
ESCALATION_FEE = 50       # extra fee when overdue >= 2 days (escalation)
MAX_FINE = 500            # cap total fine

# Helper functions

def pause():
    input("\nPress Enter to continue...")

def find_book_by_id(book_id):
    for b in books:
        if b["id"] == book_id:
            return b
    return None

def search_flow():
    q = input("\nEnter search keyword (title or author): ").strip().lower()
    if q == "":
        print("No input provided.")
        return
    results = [b for b in books if q in b["title"].lower() or q in b["author"].lower()]
    if not results:
        print("No results found.")
        return

    print(f"\nSearch results ({len(results)}):")
    for idx, b in enumerate(results, 1):
        print(f"{idx}. [{b['id']}] {b['title']} — {b['author']} ({'Available' if b['available'] else 'Unavailable'})")

    # Show details?
    show = input("Show details of a result? (Enter number or press Enter to return to menu): ").strip()
    if show == "":
        return
    try:
        sel = int(show) - 1
        if sel < 0 or sel >= len(results):
            print("Invalid selection.")
            return
        book = results[sel]
        show_book_details_and_borrow(book)
    except:
        print("Invalid input.")

def show_book_details_and_borrow(book):
    print("\n--- Book Details ---")
    print("ID:", book["id"])
    print("Title:", book["title"])
    print("Author:", book["author"])
    print("Status:", "Available" if book["available"] else "Unavailable")

    if not book["available"]:
        print("This book is currently unavailable.")
        return

    borrow_choice = input("Borrow this book? (y/N): ").strip().lower()
    if borrow_choice != "y":
        return

    # Borrow form (ID no, email, contact, borrowing period)# Borrower full name
    while True:
        borrower_name = input("Borrower full name: ").strip()
        if borrower_name != "":
            break
        print("Name cannot be blank. Please try again.")

# Borrower ID number
    while True:
        borrower_id = input("Borrower ID number: ").strip()
        if borrower_id != "":
            break
        print("ID number cannot be blank. Please try again.")

# Borrower email
    while True:
        borrower_email = input("Borrower email: ").strip()
        if borrower_email != "":
            break
        print("Email cannot be blank. Please try again.")

# Borrower contact number
    while True:
        borrower_contact = input("Contact number: ").strip()
        if borrower_contact != "":
            break
        print("Contact number cannot be blank. Please try again.")
    

    try:
        days = int(input("Borrowing period in days (e.g., 7): ").strip())
        if days <= 0:
            raise ValueError()
    except:
        print("Invalid period, defaulting to 7 days.")
        days = 7

    borrow_date = datetime.date.today()
    due_date = borrow_date + datetime.timedelta(days=days)

    # Confirm borrowing
    print("\nConfirm borrowing:")
    print(f"Book: {book['title']}")
    print(f"Borrower: {borrower_name} (ID: {borrower_id})")
    print(f"Borrow period: {days} day(s). Due date: {due_date}")
    confirm = input("Confirm? (y/N): ").strip().lower()
    if confirm != "y":
        print("Borrowing cancelled.")
        return

    record = {
        "transaction": "borrow",
        "book_id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "borrower_name": borrower_name,
        "borrower_id": borrower_id,
        "email": borrower_email,
        "contact": borrower_contact,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "returned": False,
        "return_date": None,
        "fine": 0
    }

    active_borrows.append(record)
    history.append(record)
    book["available"] = False

    print("Borrowing recorded. Returning to menu.")
    return

def book_list_flow():
    print("\n--- Book List (A–Z) ---")
    sorted_books = sorted(books, key=lambda x: x["title"].lower())
    for idx, b in enumerate(sorted_books, 1):
        print(f"{idx}. [{b['id']}] {b['title']} — {b['author']} ({'Available' if b['available'] else 'Unavailable'})")

    # Option to select book to borrow
    sel = input("Enter number to view details / borrow, or press Enter to return: ").strip()
    if sel == "":
        return
    try:
        idx = int(sel) - 1
        if idx < 0 or idx >= len(sorted_books):
            print("Invalid selection.")
            return
        book = sorted_books[idx]
        # follow same detail & borrow flow
        show_book_details_and_borrow(book)
        # After borrow, ask Borrow another?
        while True:
            more = input("Borrow another book? (y/N): ").strip().lower()
            if more == "y":
                # show only available books
                available_books = [b for b in sorted_books if b["available"]]
                if not available_books:
                    print("No more available books.")
                    break
                print("\nAvailable books to choose from:")
                for i, ab in enumerate(available_books, 1):
                    print(f"{i}. [{ab['id']}] {ab['title']}")
                sel2 = input("Enter number to borrow or press Enter to stop: ").strip()
                if sel2 == "":
                    break
                try:
                    sel2i = int(sel2) - 1
                    if sel2i < 0 or sel2i >= len(available_books):
                        print("Invalid.")
                        continue
                    show_book_details_and_borrow(available_books[sel2i])
                except:
                    print("Invalid input.")
            else:
                break
    except:
        print("Invalid input.")

def history_flow():
    print("\n--- Borrowing History (most recent first) ---")
    if not history:
        print("No history records.")
        return
    # show most recent first
    for rec in reversed(history):
        if rec["transaction"] == "borrow":
            returned = "Yes" if rec.get("returned") else "No"
            print(f"[BORROW] {rec['title']} | Borrower: {rec['borrower_name']} | Borrowed: {rec['borrow_date']} | Due: {rec['due_date']} | Returned: {returned} | Fine: {rec.get('fine',0)}")
        else:
            # Shouldn't have other types in history in this simple program
            print(rec)

def return_and_fine_manager():
    print("\n--- Book Return & Fine Manager ---")
    # list currently borrowed
    if not active_borrows:
        print("No borrowed books at the moment.")
        return

    for idx, r in enumerate(active_borrows, 1):
        due = r["due_date"]
        print(f"{idx}. [{r['book_id']}] {r['title']} | Borrower: {r['borrower_name']} | Due: {due}")

    try:
        sel = int(input("Enter number to manage/check return or press Enter to cancel: ").strip())
        idx = sel - 1
        if idx < 0 or idx >= len(active_borrows):
            print("Invalid selection.")
            return
    except:
        print("Cancelled.")
        return

    record = active_borrows[idx]
    today = datetime.date.today()
    due = record["due_date"]
    days_to_due = (due - today).days
    print(f"\nSelected: {record['title']} borrowed by {record['borrower_name']}")
    print(f"Borrow date: {record['borrow_date']}, Due date: {due}")

    # Pre-due reminder?
    if days_to_due == 1:
        print("Pre-due reminder: Book is due tomorrow.")
    elif days_to_due > 1:
        print(f"Not due yet. {days_to_due} day(s) remaining.")
    elif days_to_due == 0:
        print("Due today.")
    else:
        overdue_days = (today - due).days
        print(f"Book is overdue by {overdue_days} day(s).")

    # Ask if processing return now
    action = input("Process return now? (y/N) or type 'notify' to send overdue notification: ").strip().lower()
    if action == "notify":
        if today <= due:
            print("Not overdue yet. No overdue notification sent.")
        else:
            overdue_days = (today - due).days
            print(f"Sending overdue notification to {record['borrower_name']}. Overdue by {overdue_days} days.")
            if overdue_days >= 2:
                print("Overdue >= 2 days. Sending escalation message as per flowchart.")
        return
    if action != "y":
        print("No action taken.")
        return

    # Process return flow and fine calculation with possible delay/recalculation
    if today <= due:
        # returned on time or early
        record["returned"] = True
        record["return_date"] = today
        record["fine"] = 0
        # update book availability
        b = find_book_by_id(record["book_id"])
        if b:
            b["available"] = True
        # record return in history as separate entry
        history.append({
            "transaction": "return",
            "book_id": record["book_id"],
            "title": record["title"],
            "borrower_name": record["borrower_name"],
            "return_date": today,
            "fine": 0
        })
        # remove from active borrows
        active_borrows.pop(idx)
        print("Book returned on time. No fine.")
        return

    # overdue: offer delay (recalculate)
    overdue_days = (today - due).days
    print(f"Book is overdue by {overdue_days} day(s).")

    # Offer Delay (simulate recalculation)
    delay_choice = input("Delay (recalculate overdue period)? (y/N): ").strip().lower()
    if delay_choice == "y":
        try:
            extra_days = int(input("Enter number of delay days to simulate (e.g., 1): ").strip())
            if extra_days < 0:
                extra_days = 0
        except:
            extra_days = 0
        # simulate we waited extra_days more before processing return
        simulated_date = today + datetime.timedelta(days=extra_days)
        overdue_days = (simulated_date - due).days
        print(f"After delay simulation, overdue is {overdue_days} day(s) (processing return on {simulated_date}).")
        proc_date = simulated_date
    else:
        proc_date = today

    # Now calculate fine using custom rule:
    base_fine = overdue_days * FINE_PER_DAY
    escalation = ESCALATION_FEE if overdue_days >= 2 else 0
    total_fine = base_fine + escalation
    if total_fine > MAX_FINE:
        total_fine = MAX_FINE

    # finalize return
    record["returned"] = True
    record["return_date"] = proc_date
    record["fine"] = total_fine

    # update book availability
    b = find_book_by_id(record["book_id"])
    if b:
        b["available"] = True

    # record return entry in history
    history.append({
        "transaction": "return",
        "book_id": record["book_id"],
        "title": record["title"],
        "borrower_name": record["borrower_name"],
        "return_date": proc_date,
        "fine": total_fine
    })

    # remove from active list
    active_borrows.pop(idx)

    print(f"Return processed. Overdue days: {overdue_days}. Fine: ₱{total_fine}.")
    if escalation > 0:
        print("Escalation message was sent due to >= 2 days overdue (as per flowchart).")

def exit_flow():
    print("\nRecording transactions and exiting the system.")
    print("Final transaction count:", len(history))
    print("Goodbye!")

# -----------------------------
# Main Menu
# -----------------------------
def main_menu():
    while True:
        print("\n===== LIBRARY BORROWING SYSTEM =====")
        print("\n===== Menu =====")
        print("1. Search")
        print("2. Book list (A–Z)")
        print("3. History")
        print("4. Book return & fine manager")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            search_flow()
        elif choice == "2":
            book_list_flow()
        elif choice == "3":
            history_flow()
        elif choice == "4":
            return_and_fine_manager()
        elif choice == "5":
            exit_flow()
            break
        else:
            print("Invalid choice. Please select 1-5.")
        # loop goes back to Menu as per flowchart

if __name__ == "__main__":
    main_menu()
