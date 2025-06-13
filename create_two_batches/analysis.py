import pandas as pd

df = pd.read_csv("combinations.csv")

batch1 = df[(df["Feat. Imp. (C)"] == 1) | (df["Feat. Contri (E)"] == 1)].copy()
batch2 = df[(df["Feat. Imp. (C)"] == 2) | (df["Feat. Contri (E)"] == 2)].copy()

assigned_indices = set(batch1.index).union(set(batch2.index))
unassigned = df[~df.index.isin(assigned_indices)].reset_index(drop=False)

for i, row in unassigned.iterrows():
    if i % 2 == 0:
        batch1 = pd.concat([batch1, pd.DataFrame([row.drop("index")])], ignore_index=True)
    else:
        batch2 = pd.concat([batch2, pd.DataFrame([row.drop("index")])], ignore_index=True)

batch1.to_csv("batch1.csv", index=False)
batch2.to_csv("batch2.csv", index=False)

print(f"Batch1: {len(batch1)} rows")
print(f"Batch2: {len(batch2)} rows")
