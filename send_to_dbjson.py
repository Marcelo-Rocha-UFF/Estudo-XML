import sys
import json

# creating the json file
def create_json_file(interaction_name, output):
    file_out_name = interaction_name + '.json'
    file_out = open(file_out_name, "w")
    file_out.write(output)
    # file_out.write(output.encode('utf-8')) para rodar no raspberry
    file_out.close()

def send_to_dbjson(output):
    print("Inserting interaction...")
    # inserting json file in lowdb interaction database
    dbfile = open('db.json', 'r')

    # transforma o arquivo de texto em um dict
    eva_db_dict = json.load(dbfile)

    # output é uma string. a função json.loads transforma a string em um dict
    eva_db_dict["interaccion"].append(json.loads(output))

    with open('db.json', 'w') as fp:
        json.dump(eva_db_dict, fp)

    # eva_db_dict["interaccion"].remove("EvaML_X")
    print("\nTotal interactions found:", len(eva_db_dict["interaccion"]))
