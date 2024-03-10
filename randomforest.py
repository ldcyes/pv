import numpy as np

# 生成一些示例数据
# 特征包括：年龄、性别、收入
# 假设每个特征对应一个索引
# 0: 年龄, 1: 性别, 2: 收入
# 数据格式：[年龄, 性别, 收入, 是否购买(1表示购买，0表示不购买)]
data = np.array([
    [25, 1, 50000, 1],
    [35, 0, 60000, 0],
    [45, 1, 75000, 1],
    [20, 0, 35000, 0],
    [30, 1, 80000, 1],
    [40, 0, 90000, 1],
    [50, 1, 95000, 1],
    [55, 0, 40000, 0],
    [60, 1, 85000, 1],
    [23, 0, 45000, 0]
])

# 定义随机森林的参数
num_trees = 3
max_depth = 3
num_features = 2  # 在每棵树中随机选择的特征数量

# 定义一个决策树节点
class Node:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None):
        self.feature_index = feature_index  # 用于分裂的特征索引
        self.threshold = threshold  # 分裂阈值
        self.left = left  # 左子节点
        self.right = right  # 右子节点
        self.value = value  # 叶节点的类别

# 定义随机森林类
class RandomForest:
    def __init__(self, num_trees, max_depth, num_features):
        self.num_trees = num_trees
        self.max_depth = max_depth
        self.num_features = num_features
        self.trees = []

    # 训练随机森林
    def fit(self, X, y):
        for _ in range(self.num_trees):
            # 随机选择特征
            selected_features = np.random.choice(range(X.shape[1]), size=self.num_features, replace=False)
            # 随机抽样
            sample_indices = np.random.choice(range(X.shape[0]), size=X.shape[0], replace=True)
            X_subset = X[sample_indices][:, selected_features]
            y_subset = y[sample_indices]
            tree = self._build_tree(X_subset, y_subset, depth=0)
            self.trees.append(tree)

    # 构建决策树
    def _build_tree(self, X, y, depth):
        # 叶节点情况
        if depth >= self.max_depth or len(set(y)) == 1:
            return Node(value=max(y, key=y.count))

        # 选择最佳分裂特征和阈值
        best_feature, best_threshold = self._find_best_split(X, y)

        # 分裂数据集
        left_indices = X[:, best_feature] < best_threshold
        right_indices = ~left_indices

        # 递归构建左右子树
        left = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return Node(feature_index=best_feature, threshold=best_threshold, left=left, right=right)

    # 寻找最佳分裂特征和阈值
    def _find_best_split(self, X, y):
        best_gini = float('inf')
        best_feature = None
        best_threshold = None

        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_indices = X[:, feature] < threshold
                gini = self._calculate_gini(y[left_indices], y[~left_indices])
                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    # 计算基尼不纯度
    def _calculate_gini(self, left, right):
        total_samples = len(left) + len(right)
        gini = 0.0

        for subset in (left, right):
            size = len(subset)
            if size == 0:
                continue
            proportion = size / total_samples
            score = 1.0
            for class_val in set(subset):
                p = (subset == class_val).sum() / size
                score -= p * p
            gini += proportion * score
        return gini

    # 预测函数
    def predict(self, X):
        predictions = []
        for tree in self.trees:
            predictions.append(self._traverse_tree(X, tree))
        # 投票决定最终的预测结果
        predictions = np.transpose(predictions)
        final_predictions = [max(set(prediction), key=prediction.count) for prediction in predictions]
        return final_predictions

    # 遍历决策树以进行预测
    def _traverse_tree(self, X, node):
        if node.value is not None:
            return node.value
        if X[node.feature_index] < node.threshold:
            return self._traverse_tree(X, node.left)
        return self._traverse_tree(X, node.right)


# 准备数据
X = data[:, :-1]
y = data[:, -1]

# 初始化随机森林模型
rf_model = RandomForest(num_trees=num_trees, max_depth=max_depth, num_features=num_features)

# 训练模型
rf_model.fit(X, y)

# 预测新数据
new_data_point = np.array([33, 1, 55000])  # 示例新数据点
prediction = rf_model.predict(new_data_point)
print("预测结果:", "购买" if prediction[0] == 1 else "不购买")
