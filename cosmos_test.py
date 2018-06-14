from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from bottle import route, run, template, redirect, request

table_service = TableService(connection_string='DefaultEndpointsProtocol=https;AccountName=k1cosmos;AccountKey=rvw8KdHLNumJp6q6JpcDSbeI1oaBNrwM7iJ1r9fVD0WeJHkL1soQAubah1J35zlV6UCgGUArvm13U3VTsFQfWQ==;TableEndpoint=https://k1cosmos.table.cosmosdb.azure.com:443/')
#flag = table_service.exists('tasktable')
#print(flag)
#if flag is True:
#    print("True=" + str(flag))
#    table_service.delete_table('tasktable')
#    table_service.create_table('tasktable')
#    task = {'PartitionKey': 'tasksSeattle', 'RowKey': '001', 'description' : 'Take out the trash', 'priority' : 200}
#    table_service.insert_entity('tasktable', task)
#else:
#    print("Else2")
#table_service.create_table('tasktable2')
#task = {'PartitionKey': 'tasksSeattle2', 'RowKey': '005', 'description' : 'Take out the trash', 'priority' : 200}
#table_service.insert_entity('tasktable2', task)
#tasks = table_service.query_entities('tasktable2', filter="PartitionKey eq 'tasksSeattle2'")

# / にアクセスしたら、index関数が呼ばれる
@route("/")
def index():
    todo_list = get_todo_list()
    return template("Azure_test/index", todo_list=todo_list)

# methodにPOSTを指定して、add関数を実装する
@route("/add", method="POST")
def add():
    todo = request.forms.getunicode("todo_list")
    save_todo(todo)
    return redirect("/")

# @routeデコレータの引数で<xxxx>と書いた部分は引数として関数に引き渡すことができます。
# intは数字のみ受け付けるフィルタ
@route("/delete/<todo_id>")
def delete(todo_id):
    delete_todo(todo_id)
    return redirect("/")

def get_todo_list():
    todo_list = []
    tasks = table_service.query_entities('tasktable2', filter="PartitionKey eq 'tasksSeattle2'")
    for task in tasks:
        todo_list.append({"id": task.RowKey,"todo": task.description})
    #todo_list.append({"todo": task.description})
    #print(todo_list)
    return todo_list

def save_todo(todo):
    task = {'PartitionKey': 'tasksSeattle2', 'RowKey': '003', 'description' : todo, 'priority' : 200}
    table_service.insert_entity('tasktable2', task)

def delete_todo(todo_id):
    #todo_tmp = "003"
    print(todo_id)
    table_service.delete_entity('tasktable2', 'tasksSeattle2', todo_id)

#テスト用のサーバをlocalhost:8080で起動する
run(host="localhost", port=8080, debug=True, reloader=True)