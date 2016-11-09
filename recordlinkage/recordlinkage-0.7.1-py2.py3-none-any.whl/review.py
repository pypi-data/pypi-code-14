import json
import pandas

def review_json(df1, df2, comparison_vectors, classification=None, fields=None):

	trees_str = []

	for comp_ind, vectors in comparison_vectors.iterrows():

		index_a = comp_ind[0]
		index_b = comp_ind[1]

		if classification:
			cl_matching = classification.loc[comp_ind]
		else:
			cl_matching = None

		source_records = df1.loc[index_a].to_frame().to_json()
		target_records = df2.loc[index_b].to_frame().to_json()

		linkbox = {
			"compare": [],
			"target": {},
			"source": {},
			"_match": cl_matching,
		}

		for key, value in vectors.iteritems():

			x = {
				"_target": key,
				"_source": key,
				"_type": "number",
				"value": None
			}

			linkbox["compare"].append(x)

		tree_str = """{{\"source\": {},\"target\":{},\"links\":[{}]}} """.format(source_records, target_records, json.dumps(linkbox))
		trees_str.append(tree_str)
		# print (tree_str)

	forest_str = """{{"forest": {{ "tree": [{}]}}}}""".format(','.join(trees_str))

	return forest_str


df1 = pandas.DataFrame([[1,2,3,4,5,6,7,8], [2,3,4,5,6,7,8,9]])
df2 = pandas.DataFrame([[1,2,3,4,5,6,7,8], [2,3,4,5,6,7,8,9]])

comparison_vectors = pandas.DataFrame([[0,1,3, 4,5 ,6], [1,0,4, 5,6,7]])
comparison_vectors.set_index([0,1], inplace=True)

matches = pandas.Series([0, 1], index=comparison_vectors.index)

# print df1
# print comparison_vectors

print review_json(df1, df2, comparison_vectors)

