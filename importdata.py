# main_importer.py (formerly importdata.py)

# --- 1. Import the Neo4j Connector ---
# CORRECTED: Changed 'neo4j_connector' to 'neo4jconnector' based on your clarification
from neo4jconnector import FinancialKnowledgeGraph

# --- 2. Import Your Data Definition Functions ---
# You need to make sure these files exist in the same directory as this script
# and contain the 'add_...' functions as defined in your original documents.

# From 'Pre 1800 history' document
# Ensure you've saved the Python code from this document into 'pre_1800_history.py'
from pre_1800_history import add_historical_financial_evolution

# From 'PAnic of 1873' document
# Ensure you've saved the Python code from this document into 'panic_of_1873.py'
from panic_of_1873 import add_panic_1873_long_depression

# From 'Modern Macro events' document
# Ensure you've saved the Python code from this document into 'modern_macro_events.py'
from modern_macro_events import add_modern_macro_event_nodes

# --- IMPORTS FOR NEWLY PROVIDED DOCUMENTS ---
# For 'temporal tag matcher' - you'll likely extract REASONING_PATH_TAGS as nodes/properties
# from temporal_tag_matcher import REASONING_PATH_TAGS # Example if you want to access raw dict
# You'll need a function like `add_reasoning_paths(kg)`

# For 'Financial mathmatics' (financial_math_kg.py)
# This one is special. It defines a class (FinancialMathKG) that *builds its own graph*.
# To integrate, you'll need to either:
#   A) Modify `financial_math_kg.py` so its `add_formula` calls `kg.create_node` and `kg.create_relationship` directly,
#      passing your `FinancialKnowledgeGraph` (kg) instance into it.
#   B) Add a new function to `financial_math_kg.py` (e.g., `extract_math_graph_data`) that returns
#      lists of nodes and relationships in a format your `kg.create_node`/`create_relationship` can consume.
#   C) Create an entirely new Python file (e.g., `financial_math_data_extractor.py`) that imports `FinancialMathKG`
#      and then iterates through its internal graph to call `kg.create_node` and `kg.create_relationship`.
#
# For now, I'll add a placeholder import assuming you'll create a new `add_financial_math_formulas_to_kg` function
# from financial_math_kg_extractor import add_financial_math_formulas_to_kg # This file/function needs to be created


# For 'echo path visualizer' - contains historical_nodes and reasoning_paths data, and edges
# You'll want to extract these lists into a function, e.g., `add_echo_path_data(kg)`
# from echo_path_visualizer_data import add_echo_path_data # This file/function needs to be created

# For 'historical index scorer' - contains HISTORICAL_LINKS data
# You'll want to extract this into nodes/relationships/properties
# from historical_index_scorer_data import add_historical_echo_index_data # This file/function needs to be created


# --- OTHER DOCUMENTS YOU MENTIONED (Need to process these similarly) ---
# - intelligent compounder engine (likely data about financial instruments, scores)
# - regime simulator (macro snapshots, regime templates, path maps)
# - back test performance list (backtest results, alerts - likely logging *to* BigQuery/other DB)
# - log backtest trends (logging backtest results - likely logging *to* BigQuery/other DB)
# - Timing Harmony (system health data - likely logging *to* BigQuery/other DB)

# For performance and logging data (like backtest results, timing harmony, compounder scores),
# Neo4j might store the metadata (e.g., a node for 'Backtest Run' linked to 'ReasoningPath'),
# but the raw time-series performance data might be better suited for BigQuery.
# Consider a hybrid approach where Neo4j stores the *relationships* between these concepts,
# and BigQuery stores the *raw performance metrics*.


# --- 3. Configuration for Your Neo4j Database ---
# IMPORTANT: Replace these with your actual Neo4j connection details.
# If using Neo4j Desktop, make sure your database is running.
# If using AuraDB, ensure your IP address is whitelisted and use the provided URI/credentials.
NEO4J_URI = "bolt://localhost:7687"  # Example: "bolt://123.45.67.89:7687" for AuraDB
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "your_neo4j_password" # <<<--- REPLACE THIS WITH YOUR REAL PASSWORD


if __name__ == "__main__":
    kg = None  # Initialize kg to None for safety

    try:
        # Initialize the knowledge graph connector
        print("Attempting to connect to Neo4j...")
        kg = FinancialKnowledgeGraph(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

        # OPTIONAL BUT RECOMMENDED: Clear the database for a fresh start
        # Use with EXTREME CAUTION, especially in production environments!
        # Uncomment the line below ONLY if you want to wipe all existing data before import.
        # kg.clear_database() # Consider uncommenting if you're frequently re-importing

        # Create necessary uniqueness constraints
        # This is very important for performance and data integrity. Run this once
        # per new database or after clearing it.
        print("\nCreating Neo4j uniqueness constraints...")
        kg.create_constraints()

        # --- 4. Call Your Data Definition Functions to Populate the Graph ---
        print("\n--- Starting Data Import ---\n")

        # Add historical financial evolution data
        print("Adding Pre-1800 financial evolution data...")
        add_historical_financial_evolution(kg)

        # Add Panic of 1873 and Long Depression data
        print("Adding Panic of 1873 and Long Depression data...")
        add_panic_1873_long_depression(kg)

        # Add Modern Macro events data
        print("Adding Modern Macro events data...")
        add_modern_macro_event_nodes(kg)

        # --- Placeholder calls for your other data imports ---
        # As you process each of your 20+ documents, you will:
        # 1. Create a new Python file (e.g., 'financial_math_data.py') to house its data
        #    and an `add_...` function that calls `kg.create_node` and `kg.create_relationship`.
        # 2. Add an `import` statement at the top of this `main_importer.py`.
        # 3. Add a call to that `add_...` function here.

        # Example: Adding Financial Mathematics formulas (assuming you implement `add_financial_math_formulas_to_kg`)
        # print("Adding Financial Mathematics formulas...")
        # add_financial_math_formulas_to_kg(kg)

        # Example: Adding Echo Path data (assuming you implement `add_echo_path_data`)
        # print("Adding Echo Path visualizer data...")
        # add_echo_path_data(kg)

        # Example: Adding Historical Index Scorer data (assuming you implement `add_historical_echo_index_data`)
        # print("Adding Historical Echo Index data...")
        # add_historical_echo_index_data(kg)

        # Note: For documents like 'back test performance list', 'log backtest trends',
        # 'intelligent compounder engine', and 'Timing Harmony', they might contain
        # data that is more transactional or time-series based. For these, consider:
        #   - Creating nodes/relationships in Neo4j for the *entities* involved (e.g., `(:Backtest)`, `(:Portfolio)`, `(:SystemMetric)`).
        #   - Storing the actual *performance numbers* or *time-series logs* in BigQuery
        #     or another suitable database, and linking to them from Neo4j nodes (e.g., a `Backtest` node in Neo4j might have a property `bigquery_table_id: 'my_project.backtest_results.run_123'`).


        print("\n--- Data Import Complete ---\n")
        print("✅ All specified data imported to Neo4j successfully!")

    except Exception as e:
        print(f"❌ An error occurred during Neo4j import: {e}")
        # It's helpful to import traceback for more detailed error analysis in debugging
        import traceback
        traceback.print_exc() # This will print the full stack trace of the error
    finally:
        # Ensure the connection is closed even if an error occurs
        if kg:
            kg.close()
