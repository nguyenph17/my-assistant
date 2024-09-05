"""
title: Llama Index DB Pipeline
author: 0xThresh
date: 2024-07-01
version: 1.0
license: MIT
description: A pipeline for using text-to-SQL for retrieving relevant information from a database using the Llama Index library.
requirements: llama_index, sqlalchemy, psycopg2-binary
"""

from typing import List, Union, Generator, Iterator
import os 
from pydantic import BaseModel
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import SQLDatabase, PromptTemplate
from sqlalchemy import create_engine
from llama_index.llms.openai import OpenAI
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)


from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


class Pipeline:
    class Valves(BaseModel):
        DB_HOST: str
        DB_PORT: str
        DB_USER: str
        DB_PASSWORD: str        
        DB_DATABASE: str
        DB_TABLES: list[str]
        TEXT_TO_SQL_MODEL: str 


    # Update valves/ environment variables based on your selected database 
    def __init__(self):
        self.name = "Database RAG Pipeline"
        self.engine = None
        self.nlsql_response = ""

        # Initialize
        self.valves = self.Valves(
            **{
                "pipelines": ["*"],                                 # Connect to all pipelines
                "DB_HOST": os.environ["PG_HOST"],                   # Database hostname
                "DB_PORT": os.environ["PG_PORT"],                   # Database port 
                "DB_USER": os.environ["PG_USER"],                   # User to connect to the database with
                "DB_PASSWORD": os.environ["PG_PASSWORD"],           # Password to connect to the database with
                "DB_DATABASE": os.environ["PG_DB"],                 # Database to select on the DB instance
                "DB_TABLES": ["orders", "order_lines", "customers"],                 # Table(s) to run queries against 
                "TEXT_TO_SQL_MODEL": os.environ["TEXT_TO_SQL_MODEL"]# Model to use for text-to-SQL generation      
            }
        )

    def init_db_connection(self):
        # Update your DB connection string based on selected DB engine - current connection string is for Postgres
        self.engine = create_engine(f"postgresql+psycopg2://{self.valves.DB_USER}:{self.valves.DB_PASSWORD}@{self.valves.DB_HOST}:{self.valves.DB_PORT}/{self.valves.DB_DATABASE}")
        return self.engine

    async def on_startup(self):
        # This function is called when the server is started.
        self.init_db_connection()

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # Debug logging is required to see what SQL query is generated by the LlamaIndex library; enable on Pipelines server if needed
        self.init_db_connection()
        # Create database reader for Postgres
        sql_database = SQLDatabase(self.engine, include_tables=self.valves.DB_TABLES)

        llm = OpenAI(temperature=0.1, model=self.valves.TEXT_TO_SQL_MODEL)

        with open("/mnt/c/Projects/my-assistant/pipelines/data/data_desc.json", "r") as schema_file:
            schema_desc = schema_file.read()

        # Set up the custom prompt used when generating SQL queries from text
        text_to_sql_prompt = """
        Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. 
        You can order the results by a relevant column to return the most interesting examples in the database.
        Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per Postgres. You can order the results to return the most informative data in the database.
        Never query for all the columns from a specific table, only ask for a few relevant columns given the question.
        You should use DISTINCT statements and avoid returning duplicates wherever possible.
        Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Pay attention to which column is in which table. Also, qualify column names with the table name when needed. You are required to use the following format, each taking one line:

        Question: Question here
        SQLQuery: SQL Query to run
        SQLResult: Result of the SQLQuery
        Answer: Final answer here

        Only use tables listed below.
        {schema}

        Tables and columns description:
        ```json
        {{
            "orders": {{
                "description": "The `orders` table stores information about customer orders, including details about the order's status, timing, pricing, and associated metadata.",
                "column": "id: Unique identifier for each order record (primary key)\ncompany_code: Code identifying the company associated with the order\nsource_store_key: Identifier for the store where the order originated\nsource_store_name: Name of the store where the order originated\norder_created_time_07: Timestamp when the order was created\norder_finished_time_07: Timestamp when the order was completed (can be null)\norder_id: Unique identifier for the order (must be unique across all orders)\norder_return_id: Identifier for any associated return order\norder_status: Current status of the order (e.g., pending, shipped, delivered)\nsub_status_code: Additional status information (can be null)\ncreated_by: Identifier or name of the user who created the order\nchannel_code: Code identifying the sales channel used for the order\nsub_status: Detailed status information (can be null)\ncustomer_phone_number: Contact phone number of the customer\nprice_rule_order_title: Title of any pricing rule applied to the order (can be null)\nspecial_order_type: Indicates if the order is of a special type (can be null)\nreason: Reason for the order or any special conditions\ndiscount_code_order: Discount code applied to the entire order (can be null)\ncustomer_id: Unique identifier for the customer who placed the order\nprice_rule_order_id: Identifier for the pricing rule applied to the order (can be null)\ntotal: Total amount of the order before discounts\ntotal_after_discount: Total amount of the order after applying discounts\ntotal_discount_amount: Total amount of discounts applied to the order\norder_amount_after_discount: Final order amount after all discounts\npaid_amount: Amount paid by the customer\nattributed_source_store_key: Key of the store attributed to the sale (can be null)\nattributed_channel_code: Code of the channel attributed to the sale (can be null)"
            }},
            "order_lines": {{
                "description": "The `order_lines` table stores information about individual items within an order, including pricing, discounts, and product details.",
                "column": "id: Unique identifier for each order line record (primary key)\norder_line_id: Unique identifier for the order line (must be unique across all order lines)\norder_id: Foreign key referencing the associated order in the Orders table\nprice_rule_order_line_title: Title of any pricing rule applied to this specific order line (can be null)\ndiscount_code_order_line: Discount code applied to this specific order line (can be null)\nvariant_id: Identifier for the product variant\nquantity: Number of items of this product/variant in the order\nprice_rule_order_line_id: Identifier for the pricing rule applied to this order line (can be null)\nproduct_discount: Discount amount applied to this product\ntax_line: Tax amount for this order line\nproduct_amount_after_discount: Final amount for this product after applying discounts\nnet_amount_no_vat: Net amount for this order line excluding VAT\nprice: Original price of the product\nprice_in_order: Price of the product as it appears in the order (may differ from original price due to discounts or promotions)",
                "relationship": "The `orders` table has a one-to-many relationship with the `order_lines` table, represented by the order_lines relationship in the Order class and the order relationship in the OrderLine class."
            }},
            "customers": {{
                "description": "The `customers` table stores comprehensive information about customers, including their personal details, contact information, geographical location, and classification within the system.",
                "column": "customer_id: Unique identifier for each customer (primary key)\ncustomer_code: A code assigned to the customer, possibly for internal reference\ncreated_date_07: The date when the customer record was created\nbirthday_date_07: The customer's birthday (can be null)\ngroup_id: Identifier for the customer group (can be null)\ngroup_name: Name of the customer group (can be null)\nlevel_id: Identifier for the customer's level or tier (can be null)\nlevel_name: Name of the customer's level or tier (can be null)\ntype_id: Identifier for the customer type (can be null)\ntype_name: Name of the customer type (can be null)\nemail: Customer's email address (can be null)\nfull_name: Customer's full name (can be null)\ngender: Customer's gender (can be null)\nphone: Customer's phone number (can be null)\nstatus: Current status of the customer (can be null)\ncountry: Customer's country of residence (can be null)\ncity: Customer's city of residence (can be null)\ndistrict: District within the city where the customer resides (can be null)\nward: Smaller administrative division where the customer resides (can be null)\nfull_address: Complete address of the customer (can be null)\neligible_for_contact: Boolean indicating whether the customer can be contacted for marketing or other purposes (can be null)"
            }}
        }}
        ```

        Question: {query_str}
        SQLQuery: 
        """

        text_to_sql_template = PromptTemplate(text_to_sql_prompt)

        query_engine = NLSQLTableQueryEngine(
            sql_database=sql_database, 
            tables=self.valves.DB_TABLES, 
            llm=llm, 
            embed_model="local", 
            text_to_sql_prompt=text_to_sql_template, 
            # streaming=True
        )

        response = query_engine.query(user_message)
        print(response)
        print(response.metadata['sql_query'])
        # return response.response_gen
        return response
    

if __name__ == "__main__":
    pipeline = Pipeline()
    # pipeline.pipe("Top 3 customers including name and id who spent the most and how much did they spend?", "text-to-sql-model", [], {})
    pipeline.pipe("Please provide the 3 most purchased products (product_id, price, total quantity)", "text-to-sql-model", [], {})