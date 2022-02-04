import xml.etree.ElementTree as ET
import xmlschema # xmlschema validation

# schema validation
# este trecho de codigo valida o xml
# podem ocorrer dois tipos de erro (1) xml mal-formado (2) erro de validação
schema = xmlschema.XMLSchema("EvaML-Schema/evaml_schema.xsd")

tree = None # objeto vazio

def evaml_validator(evaml_file):
  global tree
  try:
    valido = True
    val = schema.iter_errors(evaml_file)
    for idx, validation_error in enumerate(val, start=1):
      print(f'[{idx}] path: {validation_error.path} | reason: {validation_error.reason}')
      valido = False
  except Exception as e:
    print(e)
    return tree
  else:
    if valido == True:
      tree = ET.parse(evaml_file)
      return tree
    else:
      return tree

""" for l in range(len(errors)):
  print(errors[l]) """
""" import os

os.system('xmllint --noout --schema evaml_schema.xsd teste.xml') """