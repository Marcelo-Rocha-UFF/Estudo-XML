clear # no linux e' clear, no windows e' cls

echo "***************************"
echo "* EvaML - Parsing process *"
echo "***************************"
echo ""

python3 eva_macro_exp.py $1 # step 01 - expanding macros

python3 eva_node_keys.py _macro.xml # step 02 - generating keys

python3 eva_xml_links.py _node_keys.xml # step 03 - to generate xml_exe file

python3 eva_json_gen.py _xml_links.xml # step 04 - Mapping XML nodes and links to a JSON file

echo ""
# step 5 - send do json db