import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import Parser

"""
Apply Principal Component Analysis to instances.
Returns the data in the n dimensions with highest variance as numpy arrays.
Input:
	-instances is a numpy ndarray with the instances
    -n is the amount of components (n is an int between 1 and 26)
"""


def pca(instances, n):
	# Transform instances
	instances = instances.T
    # Obtain the mean
	mean = np.mean(instances, axis=1)
	mean = mean.reshape(26, 1)
    # Remove the mean
	reescaled_instances = instances - mean
    # Obtain the covariance matrix and its eigen values, vectors
	cov_matrix = np.cov(reescaled_instances)
	eig_val, eig_vect = np.linalg.eig(cov_matrix)
    # Sort the pairs (eigen value, eigen vector)
	eigen_pair = [(np.abs(eig_val[i]), eig_vect[:, i])
	               for i in range(len(eig_val))]
	eigen_pair.sort()
	eigen_pair.reverse()
	# Obtains the first n
	matrix_w = None
	for i in range(0,n-1):
		if matrix_w is None:
			matrix_w = eigen_pair[i][1].reshape(26, 1)
		else:
			matrix_w = np.hstack((matrix_w,eigen_pair[i][1].reshape(26, 1)))
    # Multiply the reescalated instances with the extracted matrix
	transformed_instances = np.dot(reescaled_instances.T, matrix_w).T
	return transformed_instances

"""
Plot the data transformed by PCA. Plot it in several plots, split by centroid and also plot all the data together.
Input:
	-transformed is the data transformed by PCA (numpy.narray)
	-labels is the centroid assignment of each instance
	-centroids is a numpy array of centroids
"""
def plot_transformed(transformed, labels, plots_folder):
	xMax = np.max(transformed[0, :])
	xMin = np.min(transformed[0, :])
	yMax = np.max(transformed[1, :])
	yMin = np.min(transformed[1, :])

	labels_number = list(set(labels))
	labels_number.sort()
	labels = np.array(labels).reshape(1, len(labels))

	transformed = np.vstack([transformed, labels])

	black = '#000000'
	colors = ['#FFB6C1', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#00FFFF', '#0000FF', '#FF00FF', '#800080',
			  '#DAA520', '#20B2AA']

	# Plot each cluster separated
	for i in labels_number:
		filter = transformed[2, :] == i
		transformed_filtered = transformed[0:2, filter]
		plt.figure()
		plt.plot(transformed_filtered[0, :], transformed_filtered[1, :], 'o', markersize=7, color=colors[i], alpha=0.5)
		plt.xlim([xMin, xMax])
		plt.ylim([yMin, yMax])
		plt.savefig(plots_folder+"/"+('cluster{num}.png'.format(num=i)))

	# Plot all clusters together
	plt.figure()
	for i in labels_number:
		filter = transformed[2, :] == i
		transformed_filtered = transformed[0:2, filter]
		plt.plot(transformed_filtered[0, :], transformed_filtered[1, :], 'o', markersize=7, color=colors[i], alpha=0.5)
	plt.title('Clusters')
	plt.xlim([xMin, xMax])
	plt.ylim([yMin, yMax])
	plt.savefig(plots_folder+"/"+'clusters.png')

if __name__ == '__main__':
	instances = Parser.parse_data()
	transformed_instances = pca(instances, 2)
	labels = instances
	plot_transformed(transformed_instances, labels)
