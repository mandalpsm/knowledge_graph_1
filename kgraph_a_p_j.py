import pandas as pd
import networkx as nx
from pyvis.network import Network

# ==========================
# Step 1: Load dataset
# ==========================
file_path = "Dataset.csv"   # replace with your file name
df = pd.read_csv(file_path, encoding="latin1")

# Drop extra unnamed column if exists
df = df.drop(columns=["Unnamed: 9"], errors="ignore")

# Use a subset for visualization (adjust size for your machine/browser)
sample_df = df.head(300)

# ==========================
# Step 2: Create Graph
# ==========================
G = nx.MultiDiGraph()

for _, row in sample_df.iterrows():
    paper_id = row["DOI"] if "DOI" in row and pd.notna(row["DOI"]) else row["Title"]

    # Paper node
    G.add_node(
        paper_id,
        label=row["Title"],
        type="Paper",
        color="red",
        shape="square"
    )

    # Authors
    if pd.notna(row.get("Author", None)):
        for author in str(row["Author"]).split(","):
            author = author.strip()
            if author:
                G.add_node(author, type="Author", color="blue", shape="dot")
                G.add_edge(author, paper_id, relation="wrote")

    # Journal
    if pd.notna(row.get("Journal", None)):
        journal = str(row["Journal"]).strip()
        if journal:
            G.add_node(journal, type="Journal", color="green", shape="diamond")
            G.add_edge(paper_id, journal, relation="published_in")

# ==========================
# Step 3: Visualization
# ==========================
net = Network(height="750px", width="100%", directed=True, notebook=False)
net.from_nx(G)

net.write_html("knowledge_graph_apj.html")
print("✅ Graph saved as knowledge_graph_apj.html (Author–Paper–Journal only)")
