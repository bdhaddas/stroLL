# class Attractions(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     attr_lat = db.Column(db.String, nullable=False)
#     attr_long = db.Column(db.String, nullable=False)
#     attractionName = db.Column(db.String(100), nullable=False)
#     attractionDescriptor = db.Column(db.String(100), nullable=False)
#     water = db.Column(db.Boolean, nullable=False)
#     green_spaces = db.Column(db.Boolean, nullable=False)
#     traffic = db.Column(db.Boolean, nullable=False)
#     buildings = db.Column(db.Boolean, nullable=False)

#     def __repr__(self):
#         return f"Attraction('{self.attractionName}', '{self.attractionDescriptor}', ('{self.latitude}','{self.longitude}')"

#Ideally this module helps generate a list of attractions pulled from the database

class AttractionRecipe:
    def __init__(self, options):

