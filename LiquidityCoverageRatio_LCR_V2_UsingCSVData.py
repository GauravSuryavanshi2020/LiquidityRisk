import pandas as pd

# File path to your CSV
file_path = r"E:\Job Application 2024\14May2025_updated CV\PwC\Calculations Demo\LCR_Calculation.csv"

# Step 1: Read portfolio from CSV
df = pd.read_csv(file_path)

# Step 2: Recalculate Effective (after haircut)
df["Effective (after haircut)"] = df["Nominal"] * (1 - df["Haircut %"])

# Step 3: Solve for final HQLA dynamically using caps
L1 = df.loc[df["Level"] == "Level 1", "Effective (after haircut)"].sum()

# From algebra: x = L1 / (1 - 0.40)
final_total_hqla = L1 / 0.6

# Cap allocations
final_level2a = 0.25 * final_total_hqla
final_level2b = 0.15 * final_total_hqla

# Step 4: Distribute caps
# Level 2A
df.loc[df["Level"] == "Level 2A", "Effective (after caps)"] = final_level2a

# Level 2B split proportionally
level2b_uncapped = df.loc[df["Level"] == "Level 2B", "Effective (after haircut)"].sum()
df.loc[df["Level"] == "Level 2B", "Effective (after caps)"] = (
    df.loc[df["Level"] == "Level 2B", "Effective (after haircut)"] / level2b_uncapped * final_level2b
)

# Level 1 unchanged
df.loc[df["Level"] == "Level 1", "Effective (after caps)"] = df.loc[df["Level"] == "Level 1", "Effective (after haircut)"]

# Step 5: Net cash outflows (adjust as needed)
outflows = 80.0
inflows = 25.0
usable_inflows = min(inflows, 0.75 * outflows)
net_outflows = outflows - usable_inflows

# Step 6: Final LCR
total_hqla_final = df["Effective (after caps)"].sum()
lcr = total_hqla_final / net_outflows * 100

print("Final HQLA:", round(total_hqla_final, 2))
print("Net Cash Outflows:", net_outflows)
print("LCR (%):", round(lcr, 2))

# Step 7: Save updated file with recalculated results
output_path = file_path.replace(".csv", "_recalculated.csv")
df.to_csv(output_path, index=False)
print(f"Updated file saved at: {output_path}")
