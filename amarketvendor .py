def prompt_quantity(item_name):
    """
    Continuously prompts the clerk for a quantity until a valid 
    numeric value strictly greater than 0.0 is entered.
    """
    unit_label = "bunches" if item_name.lower() == "matooke" else "kg"
    while True:
        user_input = input(f"Enter quantity ({unit_label}): ").strip()
        try:
            quantity = float(user_input)
            if quantity > 0.0:
                return quantity
            else:
                print(f"Error: Quantity must exceed 0.0 {unit_label}.")
        except ValueError:
            print("Error: Please enter a valid numeric value.")


def calculate_item_price(item_type, quantity, customer_type="retail"):
    """
    Calculates line item cost based on item type, quantity, 
    and customer category (retail vs. wholesale) with tier pricing and discounts.
    """
    item = item_type.lower().strip()
    customer = customer_type.lower().strip()
    
    # Standard Retail Base Prices
    retail_prices = {
        "tomatoes": 2000,
        "onions": 1500,
        "matooke": 35000
    }
    
    # Wholesale Base Prices
    wholesale_prices = {
        "tomatoes": 1400,
        "onions": 1000,
        "matooke": 25000
    }
    
    if item not in retail_prices:
        return 0.0

    if customer == "wholesale":
        if item == "matooke":
            # Wholesale matooke requires min 3 bunches; otherwise bill retail rate
            if quantity >= 3:
                return quantity * wholesale_prices["matooke"]
            else:
                return quantity * retail_prices["matooke"]
        else:
            return quantity * wholesale_prices[item]
            
    else:  # Retail Customer
        base_price = retail_prices[item]
        if item in ["tomatoes", "onions"] and quantity > 5:
            # 5% discount only on the quantity above 5 kg
            discounted_qty = quantity - 5
            standard_qty = 5
            discounted_price = base_price * 0.95
            return (standard_qty * base_price) + (discounted_qty * discounted_price)
        else:
            return quantity * base_price


def apply_market_levy_and_packaging(subtotal, needs_eco_crate=False):
    """
    Applies a mandatory 1% market council levy and optional eco-crate deposit.
    Returns a tuple of (total_due, levy_amount, crate_deposit).
    """
    crate_deposit = 5000 if needs_eco_crate else 0
    levy_amount = subtotal * 0.01
    total_due = subtotal + crate_deposit + levy_amount
    return total_due, levy_amount, crate_deposit


def run_pos_system():
    # Session Accumulators
    total_customers = 0
    total_gross_revenue = 0.0
    highest_spender = {"name": "", "bill": 0.0}
    
    print("=" * 50)
    print("           NAGUDI'S DIGITAL STALL ")
    print("=" * 50)
    
    while True:
        customer_name = input("Customer Name: ").strip()
        if not customer_name:
            customer_name = "Walk-in Customer"
            
        while True:
            customer_type = input("Customer Type (retail/wholesale): ").strip().lower()
            if customer_type in ["retail", "wholesale"]:
                break
            print("Error: Please enter either 'retail' or 'wholesale'.")
            
        basket = []
        
        # Item entry loop
        while True:
            item_choice = input("\nAdd Item (tomatoes / onions / matooke / done): ").strip().lower()
            if item_choice == "done":
                break
            if item_choice not in ["tomatoes", "onions", "matooke"]:
                print("Error: Unknown item. Choose from tomatoes, onions, matooke, or done.")
                continue
                
            qty = prompt_quantity(item_choice)
            line_price = calculate_item_price(item_choice, qty, customer_type)
            
            unit_str = "bn" if item_choice == "matooke" else "kg"
            print(f"-> Added {qty} {unit_str} of {item_choice}.")
            
            basket.append({
                "item": item_choice,
                "quantity": qty,
                "unit": unit_str,
                "price": line_price
            })
            
        if not basket:
            print("No items added for this customer. Restarting session...")
            continue
            
        # Eco crate prompt
        crate_input = input("Add reusable delivery crate? (yes/no): ").strip().lower()
        needs_crate = True if crate_input == "yes" else False
        
        # Calculate totals
        subtotal = sum(item["price"] for item in basket)
        total_due, levy, crate_dep = apply_market_levy_and_packaging(subtotal, needs_crate)
        
        # Print Itemized Receipt
        print("\n" + "-" * 50)
        print("                        RECEIPT")
        print("#STALL-042                     ")
        print(f"Customer: {customer_name} ({customer_type.upper()})")
        print("-" * 50)
        
        for item in basket:
            # Determine effective unit price for display
            unit_price_display = item["price"] / item["quantity"] if item["quantity"] > 0 else 0
            item_display_name = item["item"].capitalize()
            print(f"{item['quantity']:<5.1f} {item['unit']:<4} x {item_display_name:<10} @ {unit_price_display:,.0f} UGX = {item['price']:,.0f} UGX")
            
        print("-" * 50)
        print(f"Subtotal:                          {subtotal:,.0f} UGX")
        if needs_crate:
            print(f"Reusable Crate Deposit:            {crate_dep:,.0f} UGX")
        print(f"Market Council Levy (1%):          {levy:,.0f} UGX")
        print("-" * 50)
        print(f"TOTAL DUE:                         {total_due:,.0f} UGX")
        print("=" * 50 + "\n")
        
        # Update session records
        total_customers += 1
        total_gross_revenue += total_due
        
        if total_due > highest_spender["bill"]:
            highest_spender["name"] = customer_name
            highest_spender["bill"] = total_due
            
        # Serve next customer check
        next_customer = input("Serve next customer? (yes/no): ").strip().lower()
        if next_customer != "yes":
            break
            
    # Daily Market Close Report
    print("\n" + "=" * 50)
    print("========== DAILY MARKET CLOSE REPORT ==========")
    print(f"Total Customers Served: {total_customers}")
    print(f"Total Revenue:          {total_gross_revenue:,.0f} UGX")
    if total_customers > 0:
        print(f"Star Customer:          {highest_spender['name']} ({highest_spender['bill']:,.0f} UGX)")
    else:
        print("Star Customer:          None (No transactions recorded)")
    print("=" * 50)
print("jolly") #hello

if __name__ == "__main__":
    run_pos_system()
