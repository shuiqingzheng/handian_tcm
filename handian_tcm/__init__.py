from py2neo import Graph
from pymysql import install_as_MySQLdb

install_as_MySQLdb()

neo_graph = Graph('bolt://10.17.1.242:7687', auth=('neo4j', 'neo4j'))
