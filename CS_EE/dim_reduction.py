from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FactorAnalysis, FastICA

def standardize(x_train, x_test):
	scaler = StandardScaler()
	scaler.fit(x_train)
	x_train = scaler.transform(x_train)
	x_test = scaler.transform(x_test)
	return x_train, x_test


def apply(n_components, x_train, x_test, method):
	x_train, x_test = standardize(x_train, x_test)
	if method == "PCA":
		dimReduction = PCA(n_components=n_components)
	elif method == "FA":
		dimReduction = FactorAnalysis(n_components=n_components)
	elif method == "ICA":
		dimReduction = FastICA(n_components=n_components)
	else:
		return
	x_train = dimReduction.fit_transform(x_train)
	x_test = dimReduction.transform(x_test)
	return x_train, x_test