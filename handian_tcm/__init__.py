from py2neo import Graph
from pymysql import install_as_MySQLdb
from .constants import NEO_BOLT, NEO_USER, NEO_PASSWORD

install_as_MySQLdb()

neo_graph = Graph(NEO_BOLT, auth=(NEO_USER, NEO_PASSWORD))
