import pandas as pd                    # 1. Imports the Pandas library to handle data in table format.
from faker import Faker                # 2. Imports Faker to generate realistic names, addresses, and IDs.
import random                           # 3. Imports Random to inject "Human Chaos" (variability) into the data.
from datetime import datetime, timedelta # 4. Imports tools to handle dates and timestamps for our "Vents."

fake = Faker()                          # 5. Initializes the Faker engine.

def generate_vaell_customers(n=100):    # 6. Defines a function to create 'n' number of Vaell Inc. customers.
    customers = []                      # 7. Creates an empty list to hold our raw data particles.
    
    for _ in range(n):                  # 8. Starts a loop that runs 'n' times.
        # 9. Create a dictionary representing one 'Human' customer at Vaell Inc.
        user = {
            "user_id": fake.uuid4(),    # 10. Generates a unique digital fingerprint for the user.
            "full_name": fake.name(),   # 11. Assigns a realistic name (PII).
            "email": fake.email(),      # 12. Assigns a realistic email address.
            "signup_date": fake.date_between(start_date='-1y', end_date='today'), # 13. Random signup date within the last year.
            "account_type": random.choice(['Basic', 'Premium', 'Elite']),        # 14. Randomly assigns a service tier.
            "initial_deposit": round(random.uniform(100, 5000), 2),              # 15. Random deposit amount with 2 decimal places.
            "is_synthetic": 0           # 16. A 'Flag' identifying this as a real human (0 = Human, 1 = Shadow).
        }
        customers.append(user)          # 17. Adds the user dictionary to our customers list.
        
    return pd.DataFrame(customers)      # 18. Converts the list of dictionaries into a clean Pandas DataFrame (table).

# 19. Execution Block: Generates 100 humans and prints the first 5 to the terminal.
if __name__ == "__main__":
    df = generate_vaell_customers(100)
    print("--- Vaell Inc. Customer Onboarding (Human Baseline) ---")
    print(df.head())
def generate_vaell_customers(n=100):
    customers = []
    for _ in range(n):
        user = {
            "user_id": fake.uuid4(),
            "full_name": fake.name(),
            "email": fake.email(),
            "signup_date": fake.date_between(start_date='-1y', end_date='today'),
            "account_type": random.choice(['Basic', 'Premium', 'Elite']),
            "initial_deposit": round(random.uniform(100, 5000), 2),
            
            # --- NEW FORENSIC METADATA ---
            "session_duration_sec": random.randint(45, 600),   # 1. How long they stayed on the signup page.
            "device_id": fake.sha256()[:12],                  # 2. A shortened hardware fingerprint.
            "failed_login_attempts": random.randint(0, 3),    # 3. Humans forget passwords; ghosts rarely do.
            "ip_address": fake.ipv4(),                        # 4. Where they are "logging in" from.
            "is_synthetic": 0 
        }
        customers.append(user)
    return pd.DataFrame(customers)
def generate_vaell_shadows(n=20):        # 1. Creates a specific 'n' number of Ghost users.
    shadows = []                         # 2. Empty list to hold the adversarial records.
    
    for _ in range(n):                   # 3. Starts the loop for the 'Shadow' factory.
        user = {
            "user_id": fake.uuid4(),
            "full_name": fake.name(),
            "email": fake.email(),
            "signup_date": fake.date_between(start_date='-30d', end_date='today'), # 4. Shadows often sign up in "Bursts" (recent).
            "account_type": 'Elite',     # 5. Fixed to 'Elite' to maximize the "Leak."
            "initial_deposit": round(random.uniform(4500, 5000), 2), # 6. High deposits to look like "Whales."
            
            # --- ADVERSARIAL METADATA ---
            "session_duration_sec": 12,  # 7. NO VARIANCE. This is the "Ghost" signal.
            "device_id": "DEVC-999-VOID",# 8. Shared Device ID (simulating a server farm).
            "failed_login_attempts": 0,  # 9. Perfect authentication (Robotic).
            "ip_address": "192.168.1.100",# 10. Shared IP (simulating a proxy/VPN tunnel).
            "is_synthetic": 1            # 11. The "Red Pill" flag for our detection testing.
        }
        shadows.append(user)
        
    return pd.DataFrame(shadows)         # 12. Returns the "Dark Force" table.
if __name__ == "__main__":
    # 1. Create 100 Humans
    humans_df = generate_vaell_customers(100)
    
    # 2. Create 20 Shadows (The Leak)
    shadows_df = generate_vaell_shadows(20)
    
    # 3. Merge them into one "Company Ledger"
    vaell_ledger = pd.concat([humans_df, shadows_df]).sample(frac=1).reset_index(drop=True)
    
    print("--- VAELL INC. CONSOLIDATED LEDGER ---")
    print(vaell_ledger.head(10)) # Look for a '1' in the is_synthetic column!
    
    # 4. Save to CSV (The "Vault" for Phase 2)
    vaell_ledger.to_csv("vaell_raw_data.csv", index=False)
    print("\n[SUCCESS] 'vaell_raw_data.csv' created. The leak is now inside the system.")
