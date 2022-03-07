import pickle
import PositionTree
pt = PositionTree.Tree()
dbReader = open("database.pkl", 'wb')
pickle.dump(pt, dbReader)
dbReader.close()
