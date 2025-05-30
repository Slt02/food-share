# FoodShare

FoodShare is a food donation and sharing platform with a graphical user interface (GUI) for customers, donors, admins, and drop-off agents. The system allows users to do all the fuctionalities that are visible in the use case diagram provided.

## Some Features

- **User Roles:** Customer, Donor, Admin, Drop-off Agent
- **Registration & Login:** Secure registration and login for all roles
- **Food Requests:** Customers can request food items and track their orders
- **Food Deliveries:** Drop-off agents can distribute the food requests to the customers
- **Donations:** Donors can register donations and track their donation history
- **Inventory Management:** Admins can add, update, and view inventory items
- **Order & Delivery Tracking:** Real-time tracking of orders and deliveries
- **Reports:** Customers can make a report if something went wrong with their order
- **Statistics & Reports:** Admins can view platform statistics and generate reports
- **Account Management:** Users can update their account information

## Requirements

- Python 3.8+
- `tkinter` (for GUI)
- `mysql-connector-python` (for MySQL database)
- MySQL server (see `foodshare.sql` for schema)

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/food-share.git
   cd food-share
   ```

2. **Install dependencies:**
   ```sh
   pip install mysql-connector-python
   ```

3. **Set up the database:**
   - Create a MySQL database (e.g., `foodshare`)
   - Import the food-share.sql file in your database

4. **Configure database connection:**
   - Update database credentials in `Database.py` or relevant controller files if needed.

5. **Run the application:**
   ```sh
   python main.py
   ```

## Usage

- Launch the app and use the GUI to register as a customer or donor, or if you imported the database, you can login with the already existing credentials (of any type of user) and test with existing data.
- Customers can browse the menu, place orders, track orders, view their order history or make a report about an order. 
- Donors can register donations and track their donations .
- Admins can manage inventory, monitor requests/deliveries, view statistic & reports and create Drop-off Agent accounts.
- Drop-off agents can assign a delivery (view available requests) and update delivery status of an order.
