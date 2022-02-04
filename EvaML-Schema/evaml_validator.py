import xmlschema

errors =[]
schema = xmlschema.XMLSchema("evaml_schema.xsd")

try:
  val = schema.iter_errors("teste.xml")
  for idx, validation_error in enumerate(val, start=1):
    print(f'[{idx}] path: {validation_error.path} | reason: {validation_error.reason}')
except Exception as e:
  print(e)
else:
  for idx, validation_error in enumerate(val, start=1):
    print(f'[{idx}] path: {validation_error.path} | reason: {validation_error.reason}')

""" for l in range(len(errors)):
  print(errors[l]) """
""" import os

os.system('xmllint --noout --schema evaml_schema.xsd teste.xml') """