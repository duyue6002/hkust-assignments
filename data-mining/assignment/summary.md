CHAMELEON: A Hierarchical Clustering Algorithm Using Dynamic Modeling

problems:

1. existing hierarchical schemes do not make use of information about the nature of individual clusters being merged. 
2. schemes ignore the important information such as the aggregate interconnectivity of items in two clusters, or whereas the closeness of two clusters.

solutions:

1. model the data items as a graph, represent data using a k-nearest neighbor graph Gk.
2. dynamically model the similarity between the clusters by computing their relative inter-connectivity and relative closeness.
3. use graph partitioning to obtain the initial fine-grain clustering solution.
4. use the relative inter-connectivity and relative closeness to repeatedly combine together the sub-clusters in a hierarchical fashion.

pros and cons:

1. handle any type of data since it is not specific to a particular domain 
2. The complexity of the algorithm O(nm + n log n + m^2log m) 
3. Different domains require different measures for connectivity and closeness, etc.

