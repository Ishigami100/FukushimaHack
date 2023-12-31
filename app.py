from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver
from flask import Flask
from flask import render_template,request, redirect


retry_config = RetryConfig(retry_limit=3)
qldb_driver = QldbDriver("quick-start", retry_config=retry_config)
app = Flask(__name__)


#def create_table(transaction_executor):
 #   print("Creating a table")
 #   transaction_executor.execute_statement("CREATE TABLE People")

#def create_index(transaction_executor):
 #   print("Creating an index")
 #   transaction_executor.execute_statement("CREATE INDEX ON People(lastName)")

def insert_documents(transaction_executor, arg_1):
    print("Inserting a document")
    transaction_executor.execute_statement("INSERT INTO People ?", arg_1)

def read_documents(transaction_executor,str):
    print("Querying the table")
    cursor = transaction_executor.execute_statement("SELECT * FROM People WHERE lastName = ?",str)
                                                                                                                                          
    for doc in cursor:
        print(doc["firstName"])
        print(doc["lastName"])
        print(doc["age"])

def update_documents(transaction_executor, age, lastName):
    print("Updating the document")
    transaction_executor.execute_statement("UPDATE People SET age = ? WHERE lastName = ?", age, lastName)

# Configure retry limit to 3
#retry_config = RetryConfig(retry_limit=3)

# Initialize the driver
#print("Initializing the driver")
#qldb_driver = QldbDriver("quick-start", retry_config=retry_config)

# Create a table
#qldb_driver.execute_lambda(lambda executor: create_table(executor))

# Create an index on the table
#qldb_driver.execute_lambda(lambda executor: create_index(executor))

# Insert a document

age = 42
lastName = 'Doe'

@app.route("/insert",methods=['POST'])
def insert():
    doc_1 = { 'firstName' :request.form["name"],
            'lastName' :request.form["name-back"],
            'age' :request.form["age"],
            }
    qldb_driver.execute_lambda(lambda x: insert_documents(x, doc_1))
    print(request.form)
# Query the table
    qldb_driver.execute_lambda(lambda executor: read_documents(executor,request.form["name-back"]))
    return redirect("https://lin.ee/6mtbeNe")
#ここまでinsert

# Update the document
#age = 42
#lastName = 'Doe'

@app.route("/update")
def update():

    qldb_driver.execute_lambda(lambda x: update_documents(x, age, lastName))
    qldb_driver.execute_lambda(lambda executor: read_documents(executor))

    return "" ,200

#age = 42
#lastName = 'Doe'
#qldb_driver.execute_lambda(lambda x: update_documents(x, age, lastName))

# Query the table for the updated document
#qldb_driver.execute_lambda(lambda executor: read_documents(executor))

@app.route("/form/fukushima")
def fukushima():
    return render_template("form_fukushima.html")
@app.route("/")
def main():
    return render_template("index.html")
@app.route("/purchase")
def purchase():
    return render_template("purchase.html")
@app.route("/form/")
def form():
    return render_template("form.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)