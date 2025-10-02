import pandas as pd
import networkx as nx
from pyvis.network import Network

# Load dataset
file_path = "Dataset.csv"
df = pd.read_csv(file_path, encoding="latin1")

# Drop empty column
df = df.drop(columns=["Unnamed: 9"], errors="ignore")

# Create Graph
G = nx.MultiDiGraph()

# Iterate over rows
for _, row in df.iterrows():
    paper_id = row["DOI"]  # use DOI as unique paper ID
    
    # Add paper node
    G.add_node(paper_id, label=row["Title"], type="Paper")
    
    # Author(s)
    if pd.notna(row["Author"]):
        for author in row["Author"].split(","):
            author = author.strip()
            G.add_node(author, type="Author")
            G.add_edge(author, paper_id, relation="wrote")
    
    # Journal
    if pd.notna(row["Journal"]):
        G.add_node(row["Journal"], type="Journal")
        G.add_edge(paper_id, row["Journal"], relation="published_in")
    
    # Publisher
    if pd.notna(row["Publisher"]):
        G.add_node(row["Publisher"], type="Publisher")
        G.add_edge(row["Journal"], row["Publisher"], relation="owned_by")
    
    # Place
    if pd.notna(row["Place"]):
        G.add_node(row["Place"], type="Place")
        G.add_edge(paper_id, row["Place"], relation="from")
    
    # Keywords
    if pd.notna(row["Keywords"]):
        for kw in row["Keywords"].split(","):
            kw = kw.strip()
            G.add_node(kw, type="Keyword")
            G.add_edge(paper_id, kw, relation="about")

# -------------------------------
# Visualization using PyVis
# -------------------------------
net = Network(height="750px", width="100%", notebook=False, directed=True)
net.from_nx(G)

# Save interactive HTML
net.write_html("knowledge_graph.html")
print("✅ Knowledge graph saved as knowledge_graph.html (open in browser)")
