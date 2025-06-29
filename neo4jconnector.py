from neo4j import GraphDatabase, basic_auth

class FinancialKnowledgeGraph:
    """
    Connects to a Neo4j database and provides methods to create nodes and relationships.
    This class is designed to work with your existing `add_historical_financial_evolution`
    and `add_panic_1873_long_depression` functions.
    """
    def __init__(self, uri, username, password):
        # Initialize the Neo4j driver with the database URI and authentication details.
        # The URI typically looks like "bolt://localhost:7687" for a local instance,
        # or a specific endpoint for Neo4j AuraDB.
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(username, password))
        print(f"🔗 Connected to Neo4j at {uri}")

    def close(self):
        # Close the driver connection when done.
        if self.driver:
            self.driver.close()
            print("Connection to Neo4j closed.")

    def _run_query(self, query, parameters=None):
        # Internal method to execute a Cypher query with proper session management.
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return result

    def create_node(self, label, properties):
        """
        Creates or merges a node with the given label and properties.
        The 'name' property is used for merging to prevent duplicates,
        and other properties are set.
        """
        node_name = properties.get("name")
        if not node_name:
            raise ValueError("Nodes must have a 'name' property for creation/merging.")

        # Create or merge the node.
        # Using MERGE ensures uniqueness based on the 'name' property.
        # SET all properties from the provided dictionary.
        query = f"""
        MERGE (n:{label} {{name: $name}})
        ON CREATE SET n = $properties
        ON MATCH SET n += $properties
        RETURN n
        """
        # Ensure 'name' is also explicitly in properties for the MERGE clause's pattern matching
        params = {"name": node_name, "properties": properties}
        self._run_query(query, params)
        print(f"  Created/Merged Node: {label} - {node_name}") # Uncommented for verbose logging

    def create_relationship(self, source_name, target_name, rel_type, properties=None):
        """
        Creates a relationship between two existing nodes.
        Relies on nodes identified by their 'name' property.
        The MATCH now looks for any node with the given name, making it
        flexible for different node labels (e.g., HistoricalEvent, MacroEvent).
        """
        if properties is None:
            properties = {}

        # MATCH source and target nodes by their name, regardless of specific label.
        query = f"""
        MATCH (source {{name: $source_name}})
        MATCH (target {{name: $target_name}})
        CREATE (source)-[r:{rel_type} $properties]->(target)
        RETURN r
        """
        params = {
            "source_name": source_name,
            "target_name": target_name,
            "properties": properties
        }
        self._run_query(query, params)
        print(f"  Created Relationship: {source_name} -[{rel_type}]-> {target_name}") # Uncommented for verbose logging

    def create_constraints(self):
        """
        Ensures uniqueness constraints are set for efficient data merging.
        It's good practice to run these once before importing.
        """
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS ON (n:HistoricalEvent) ASSERT n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS ON (n:MacroEvent) ASSERT n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS ON (n:FinancialFormula) ASSERT n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS ON (n:ReasoningPath) ASSERT n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS ON (n:Tag) ASSERT n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS ON (n:Layer) ASSERT n.name IS UNIQUE"
            # Add constraints for any other node labels you introduce
        ]
        for constraint_query in constraints:
            try:
                self._run_query(constraint_query)
                print(f"Set constraint: {constraint_query}")
            except Exception as e:
                print(f"Error setting constraint {constraint_query}: {e}")

    def clear_database(self):
        """
        WARNING: Deletes ALL nodes and relationships in the database.
        Use with extreme caution, especially in production environments.
        """
        confirmation = input("Are you sure you want to delete ALL data from Neo4j? Type 'yes' to confirm: ")
        if confirmation.lower() == 'yes':
            print("Deleting all data...")
            self._run_query("MATCH (n) DETACH DELETE n")
            print("All data deleted.")
        else:
            print("Deletion cancelled.")