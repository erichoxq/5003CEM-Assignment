import random


class ICHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.collisions = 0

    def insert(self, ic_number, ic_format=None):
        # Determine which hash function to use based on IC length or format parameter
        ic_str = str(ic_number)

        # If format is specified, pad accordingly
        if ic_format == 12:
            ic_str = ic_str.zfill(12)  # Pad with leading zeros to make 12 digits
            hash_code = hash_malaysian_ic_12(ic_str)
        elif ic_format == 16:
            ic_str = ic_str.zfill(16)  # Pad with leading zeros to make 16 digits
            hash_code = hash_malaysian_ic_16(ic_str)
        else:
            # Auto-detect based on length (with padding consideration)
            if len(ic_str) <= 12:
                ic_str = ic_str.zfill(12)
                hash_code = hash_malaysian_ic_12(ic_str)
            elif len(ic_str) <= 16:
                ic_str = ic_str.zfill(16)
                hash_code = hash_malaysian_ic_16(ic_str)
            else:
                raise ValueError(f"Invalid IC length: {len(ic_str)}. Must be 12 or 16 digits or less.")

        index = hash_code % self.size

        # Check for collision
        if len(self.table[index]) > 0:
            self.collisions += 1

        # Separate chaining for collision handling
        self.table[index].append(ic_str)  # Store the padded string
        return index

    def display_sample(self):
        """Display a sample of the hash table (first 10 and last 5 entries)"""
        print(f"Hash Table with size {self.size}:")

        # Display first 11 entries (index 0-10)
        for i in range(11):
            if len(self.table[i]) == 0:
                print(f"table[{i}]")
            else:
                chain = " --> ".join(self.table[i])
                print(f"table[{i}] --> {chain}")

        print("...")

        # Display last 5 entries
        for i in range(self.size - 5, self.size):
            if len(self.table[i]) == 0:
                print(f"table[{i}]")
            else:
                chain = " --> ".join(self.table[i])
                print(f"table[{i}] --> {chain}")


def hash_malaysian_ic_12(ic_number):
    """
    Hash function for 12-digit Malaysian IC number using folding technique
    The IC number is 12 digits without dash
    Format: YYMMDD BP ###G
    """
    # Ensure IC is string format
    ic = str(ic_number)

    # Folding technique: break into 4 parts of 3 digits each
    parts = [ic[i:i + 3] for i in range(0, len(ic), 3)]

    # Convert each part to integer and sum them
    hash_value = sum(int(part) for part in parts)

    return hash_value


def hash_malaysian_ic_16(ic_number):
    """
    Hash function for 16-digit Malaysian IC number using folding technique
    The IC number is 16 digits without dash
    Format: YYYYMMDD BP ####GG
    """
    # Ensure IC is string format
    ic = str(ic_number)

    # Folding technique: break into 4 parts of 4 digits each
    parts = [ic[i:i + 4] for i in range(0, len(ic), 4)]

    # Convert each part to integer and sum them
    hash_value = sum(int(part) for part in parts)

    return hash_value


def generate_random_ic_12():
    """Generate a random 12-digit Malaysian IC number."""
    # Generate birth date (YYMMDD)
    # For 1970-2020: 1970-1999 (70-99) and 2000-2020 (00-20)
    year_choice = random.choice(['1900s', '2000s'])
    if year_choice == '1900s':
        year = random.randint(70, 99)  # 1970-1999
    else:
        year = random.randint(0, 20)  # 2000-2020

    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Safe range for all months

    # Generate birth place (BP) - random from valid codes
    bp_codes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
                36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                51, 52, 53, 54, 55, 56, 57, 58, 59]
    bp = random.choice(bp_codes)

    # Generate serial number (3 digits) and gender digit
    serial = random.randint(0, 999)
    gender = random.randint(0, 9)

    # Format as 12-digit number (return as string to preserve leading zeros)
    ic_number = f"{year:02d}{month:02d}{day:02d}{bp:02d}{serial:03d}{gender}"
    return ic_number


def generate_random_ic_16():
    """Generate a random 16-digit Malaysian IC number."""
    # Generate birth date (YYYYMMDD)
    year = random.randint(1950, 2023)  # Full year format
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Safe range for all months

    # Generate birth place (BP) - random from valid codes
    bp_codes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
                36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                51, 52, 53, 54, 55, 56, 57, 58, 59]
    bp = random.choice(bp_codes)

    # Generate serial number (4 digits) and gender digits (2 digits)
    serial = random.randint(0, 9999)
    gender = random.randint(0, 99)

    # Format as 16-digit number (return as string to preserve leading zeros)
    ic_number = f"{year:04d}{month:02d}{day:02d}{bp:02d}{serial:04d}{gender:02d}"
    return ic_number


def main():
    # Create two hash tables with sizes 1009 and 2003
    table1 = ICHashTable(1009)
    table2 = ICHashTable(2003)

    # Run 10 rounds for each IC format
    print("=" * 60)
    print("TESTING WITH 12-DIGIT IC NUMBERS")
    print("=" * 60)

    total_collisions_table1_12 = []
    total_collisions_table2_12 = []

    for round_num in range(1, 11):
        # Reset counters for each round
        table1.collisions = 0
        table2.collisions = 0

        # Clear tables
        table1.table = [[] for _ in range(table1.size)]
        table2.table = [[] for _ in range(table2.size)]

        # Insert 1000 random 12-digit ICs into both tables
        for _ in range(1000):
            ic = generate_random_ic_12()
            table1.insert(ic, 12)  # Specify 12-digit format
            table2.insert(ic, 12)

        # Record collisions for this round
        total_collisions_table1_12.append(table1.collisions)
        total_collisions_table2_12.append(table2.collisions)

    # Display sample of both tables (only for the last round)
    print("\n12-DIGIT IC - Sample of Hash Tables:")
    table1.display_sample()
    print("\n")
    table2.display_sample()

    # Calculate and display collision statistics for 12-digit
    print(f"\n12-DIGIT IC RESULTS:")
    print(f"Collision Rate for Smaller Hash Table: {(sum(total_collisions_table1_12) / 10) / 10:.2f} %")
    print(f"Collision Rate for Bigger Hash Table: {(sum(total_collisions_table2_12) / 10) / 10:.2f} %")

    # Print collision stats for each round
    print("\nCollision Statistics by Round (12-digit):")
    for i in range(10):
        print(
            f"Round {i + 1}: Table 1: {total_collisions_table1_12[i]} collisions, Table 2: {total_collisions_table2_12[i]} collisions")

    # Calculate averages for 12-digit
    avg_collisions_table1_12 = sum(total_collisions_table1_12) / 10
    avg_collisions_table2_12 = sum(total_collisions_table2_12) / 10

    print(f"\nAverage Collisions for Table 1 (size 1009): {avg_collisions_table1_12:.2f}")
    print(f"Average Collisions for Table 2 (size 2003): {avg_collisions_table2_12:.2f}")

    print("\n" + "=" * 60)
    print("TESTING WITH 16-DIGIT IC NUMBERS")
    print("=" * 60)

    total_collisions_table1_16 = []
    total_collisions_table2_16 = []

    for round_num in range(1, 11):
        # Reset counters for each round
        table1.collisions = 0
        table2.collisions = 0

        # Clear tables
        table1.table = [[] for _ in range(table1.size)]
        table2.table = [[] for _ in range(table2.size)]

        # Insert 1000 random 16-digit ICs into both tables
        for _ in range(1000):
            ic = generate_random_ic_16()
            table1.insert(ic, 16)  # Specify 16-digit format
            table2.insert(ic, 16)

        # Record collisions for this round
        total_collisions_table1_16.append(table1.collisions)
        total_collisions_table2_16.append(table2.collisions)

    # Display sample of both tables (only for the last round)
    print("\n16-DIGIT IC - Sample of Hash Tables:")
    table1.display_sample()
    print("\n")
    table2.display_sample()

    # Calculate and display collision statistics for 16-digit
    print(f"\n16-DIGIT IC RESULTS:")
    print(f"Collision Rate for Smaller Hash Table: {(sum(total_collisions_table1_16) / 10) / 10:.2f} %")
    print(f"Collision Rate for Bigger Hash Table: {(sum(total_collisions_table2_16) / 10) / 10:.2f} %")

    # Print collision stats for each round
    print("\nCollision Statistics by Round (16-digit):")
    for i in range(10):
        print(
            f"Round {i + 1}: Table 1: {total_collisions_table1_16[i]} collisions, Table 2: {total_collisions_table2_16[i]} collisions")

    # Calculate averages for 16-digit
    avg_collisions_table1_16 = sum(total_collisions_table1_16) / 10
    avg_collisions_table2_16 = sum(total_collisions_table2_16) / 10

    print(f"\nAverage Collisions for Table 1 (size 1009): {avg_collisions_table1_16:.2f}")
    print(f"Average Collisions for Table 2 (size 2003): {avg_collisions_table2_16:.2f}")

    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"12-digit IC - Table 1 avg collisions: {avg_collisions_table1_12:.2f}")
    print(f"12-digit IC - Table 2 avg collisions: {avg_collisions_table2_12:.2f}")
    print(f"16-digit IC - Table 1 avg collisions: {avg_collisions_table1_16:.2f}")
    print(f"16-digit IC - Table 2 avg collisions: {avg_collisions_table2_16:.2f}")

    print("\nProcess finished with exit code 0")


if __name__ == "__main__":
    main()