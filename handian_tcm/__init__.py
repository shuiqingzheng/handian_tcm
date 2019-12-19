from py2neo import Graph
from pymysql import install_as_MySQLdb
from .settings import RIVER_KTDB_ADDR, RIVER_KTDB_USER, RIVER_KTDB_PASSWORD

install_as_MySQLdb()

neo_graph = Graph(RIVER_KTDB_ADDR, auth=(RIVER_KTDB_USER, RIVER_KTDB_PASSWORD))
