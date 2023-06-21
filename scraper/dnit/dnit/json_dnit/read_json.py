import json

class ReadJson():

    # gets all points given the json file name
    def get_points(self, file_name):
        dic_points  = self.read_file(file_name)
        list_points = self.extract_points(dic_points)
        return list_points
    

    # read the json file
    def read_file(self,file_name):
        f = open(file_name)

        # returns JSON object as a dictionary
        data = json.load(f)
        f.close()
        return data


    # extracts points from python dictionary
    def extract_points(self, dic_json):
        list_json = dic_json["dado"]
        list_points = []

        for point in list_json:
            list_points.append(point["idPosto"])

        return list_points