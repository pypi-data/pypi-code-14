from setuptools import setup

setup(
		name = "xrpi-test-12.10.16",
		version = "0.0.2",
		description = "XGBoost powered RNA-Protein Interaction prediction",
		# url=""
		author = "Sanket Gupte",
		author_email = "sanketgupte14@gmail.com",
		license = "Not Free Stuff",
		packages = ["xrpi"],
		zip_safe = True,
		install_requires = [
								"scikit-learn",
								"xgboost",
								"numpy",
								"scipy"
						   ],
		scripts = ["bin/xrpi"]
	)
