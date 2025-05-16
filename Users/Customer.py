class Customer:
    def __init__(self, Customer_id, name, email, phone_number, adress_num ): 
        self.Customer_id = Customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.adress_num = adress_num
        
        self.order_history = []
