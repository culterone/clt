from flask import Flask, render_template, request, jsonify, json, Blueprint
from flask_sqlalchemy import SQLAlchemy
from serverside.serverside_table import ServerSideTable
from serverside import table_schemas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:abcdef@10.10.99.11/test1'
db = SQLAlchemy(app)

class table2(db.Model):
   __tablename__ = 'table2'
   cola = db.Column('A', db.String(2))
   colb = db.Column('B', db.String(2))
   colc = db.Column('C', db.Integer, primary_key=True)
   cold = db.Column('D', db.Integer)

   def __init__(self, cola, colb, colc, cold):
      self.cola = cola
      self.colb = colb
      self.colc = colc
      self.cold = cold
      pass

   @property
   def serialize(self):
      return {
         'cola': self.cola,
         'colb': self.colb,
         'colc': self.colc,
         'cold': self.cold
      }

# DB COUNT ROWS
rowsCount = table2.query.count()

# DB query and serialize
tick = table2.query.all()
data=[i.serialize for i in tick]


@app.route('/data')
def get_data():
   return render_template('data.html')


# merging dictionaries to add draw, recordsTotal..
x = {'draw':1,'recordsTotal':rowsCount,'recordsFiltered':10}
y = dict(data=[i.serialize for i in tick])

z = y.copy()
z.update(x)

@app.route("/api/result")
def result_json():
   return jsonify(z)


# Sergio's part

class TableBuilder(object):

   def collect_data_clientside(self):
      return {'data': data}

   def collect_data_serverside(self, request):
      columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
      return ServerSideTable(request, data, columns).output_result()


#@main.route("/serverside_table")
#def serverside_table():
#   print("Hello")
#   return render_template("data.html")
