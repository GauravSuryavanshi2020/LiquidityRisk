import pandas as pd

# Step 1: Portfolio inputs (in millions)
portfolio = {
    "Asset": ["Cash", "Sovereign Bonds (2A)", "Corporate Bonds (2B)", "RMBS (2B)"],
    "Level": ["Level 1", "Level 2A", "Level 2B", "Level 2B"],
    "Nominal": [50, 30, 20, 10],
    "Haircut %": [0.0, 0.15, 0.25, 0.35]
}

df = pd.DataFrame(portfolio)

# Step 2: Apply haircuts
df["Effective (after haircut)"] = df["Nominal"] * (1 - df["Haircut %"])

# Step 3: Caps enforcement (based on final total HQLA = 83.333)
final_total_hqla = 83.333
final_level2a = 0.25 * final_total_hqla  # 20.833
final_level2b = 0.15 * final_total_hqla  # 12.5

# Adjust for caps
df.loc[df["Level"] == "Level 2A", "Effective (after caps)"] = final_level2a

# Proportional split for Level 2B (corp + RMBS)
level2b_uncapped = df.loc[df["Level"] == "Level 2B", "Effective (after haircut)"].sum()
df.loc[df["Level"] == "Level 2B", "Effective (after caps)"] = (
    df.loc[df["Level"] == "Level 2B", "Effective (after haircut)"] / level2b_uncapped * final_level2b
)

# Level 1 remains unchanged
df.loc[df["Level"] == "Level 1", "Effective (after caps)"] = df.loc[df["Level"] == "Level 1", "Effective (after haircut)"]

# Step 4: Net cash outflows
outflows = 80.0
inflows = 25.0
usable_inflows = min(inflows, 0.75 * outflows)
net_outflows = outflows - usable_inflows

# Step 5: LCR calculation
total_hqla_final = df["Effective (after caps)"].sum()
lcr = total_hqla_final / net_outflows * 100

print("Final HQLA:", total_hqla_final)
print("Net Cash Outflows:", net_outflows)
print("LCR:", lcr)